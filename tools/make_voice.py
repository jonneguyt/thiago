"""Build voice.json: every phrase the page says, spoken by the Piper Dutch voice (nl rdh medium, CC0), as base64 mp3.
Single sounds ("klank:m") are synthesized from phonemes with onnxruntime and stretched, for zoemen.
Usage: python3 tools/make_voice.py <piper binary> <voice .onnx>"""
import base64, json, os, re, subprocess, sys, tempfile, wave
import numpy as np, onnxruntime as ort

piper, model = sys.argv[1], sys.argv[2]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(root, 'app.html'), encoding='utf-8').read()
names = re.findall(r"\[\d+,'([^']+)'\]", html)
entries = re.findall(r"\['([a-z]+)','[^']+','([a-z-]+)'", html)
words = [w for w, _ in entries]
graphemes = sorted({g for _, gs in entries for g in gs.split('-')})

# How a Dutch reader should pronounce the English/Japanese names
SOUND = {
 'Pikachu':'Piekatsjoe','Bulbasaur':'Bulbasor','Charmander':'Tsjarmender','Squirtle':'Skwurtul','Eevee':'Iewie',
 'Jigglypuff':'Djiggeliepuf','Psyduck':'Saaiduk','Meowth':'Mie-ouf','Snorlax':'Snorlaks','Togepi':'Toogeepie',
 'Pichu':'Pietsjoe','Magikarp':'Medjiekarp','Ditto':'Dittoo','Slowpoke':'Sloopook','Vulpix':'Vulpiks',
 'Gengar':'Genggar','Charizard':'Tsjarriezard','Dragonite':'Dreggonaait','Mew':'Mjoe','Chikorita':'Tsjiekoorieta',
 'Cyndaquil':'Sindakwil','Totodile':'Tootoodaail','Treecko':'Triekoo','Torchic':'Tortsjik','Mudkip':'Mudkip',
 'Piplup':'Piplup','Lucario':'Loekaarioo','Rowlet':'Roolet','Litten':'Litten','Popplio':'Popplieoo',
 'Sprigatito':'Spriegatietoo','Fuecoco':'Foeweekookoo','Quaxly':'Kweksli','Espeon':'Espiejon','Umbreon':'Umbriejon',
 'Leafeon':'Liefiejon','Glaceon':'Gleesiejon','Sylveon':'Silviejon',
}
NUM = ['nul','één','twee','drie','vier','vijf','zes','zeven','acht','negen','tien','elf','twaalf','dertien',
       'veertien','vijftien','zestien','zeventien','achttien','negentien','twintig']
def spoken(text):
    for n, s in SOUND.items(): text = re.sub(r'\b%s\b' % n, s, text)
    text = text.replace('Pokébal', 'Pookeebal').replace('Thiago', 'Tiejaagoo')
    return re.sub(r'\b(\d+)\b', lambda m: NUM[int(m.group(1))], text)

phrases = {}
def add(key): phrases[key] = spoken(key)
for i in range(1, 21):
    add(str(i)); add(f'{i} plus'); add(f'{i} min'); add(f'{i} is?'); add(f'{i} is')
for n in names:
    add(n); add(f'Hoeveel {n} zie je?'); add(f'Hoera! Je hebt {n} gevangen!'); add(f'{n} kwam weer langs!')
for w in words: add(w)
for p in ['Goed zo!', 'Super!', 'Knap hoor!', 'Ja, goed!', 'Top!', 'Wauw!', 'Met welke klank begint',
          'Lees het woord. Welk plaatje hoort erbij?', 'Bijna! Probeer het nog eens.', 'Er zit iets in de Pokébal!',
          'Die heb je nog niet gevangen.', 'Hoi Thiago!']:
    add(p)

# Dutch sound -> espeak phonemes. Sounds you can hold (zingend) are stretched; plosives stay short.
IPA = {'a':['ɑ'],'e':['ɛ'],'i':['ɪ'],'o':['ɔ'],'u':['ɵ'],'aa':['a','ː'],'ee':['e','ː'],'oo':['o','ː'],'oe':['u'],'ei':['ɛ','ɪ'],'ij':['ɛ','ɪ'],'ui':['œ','y'],'eu':['ø','ː'],'uu':['y','ː'],'w':['ʋ'],'h':['ɦ']}
SHORT = set('bptkd')
cfg = json.load(open(model + '.json')); pid = cfg['phoneme_id_map']
sess = ort.InferenceSession(model)
def klank_wav(g, path):
    phs = IPA.get(g, [g])
    if g not in SHORT and len(phs) == 1: phs = phs * 3
    ids = pid['^'][:]
    for ph in phs: ids += pid[ph] + pid['_']
    ids += pid['$']
    x = np.array([ids], dtype=np.int64)
    a = sess.run(None, {'input': x, 'input_lengths': np.array([x.shape[1]], dtype=np.int64),
                        'scales': np.array([0.5, 1.0 if g in SHORT else 1.8, 0.6], dtype=np.float32)})[0].squeeze()
    a = (a / max(1e-6, float(np.abs(a).max())) * 0.8 * 32767).astype(np.int16)
    w = wave.open(path, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(22050); w.writeframes(a.tobytes()); w.close()

out = {}
with tempfile.TemporaryDirectory() as tmp:
    for g in graphemes:
        wav, mp3 = os.path.join(tmp, f'k_{g}.wav'), os.path.join(tmp, f'k_{g}.mp3')
        klank_wav(g, wav)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', 'apad=pad_dur=0.25',
                        '-ac', '1', '-ar', '22050', '-b:a', '40k', mp3], check=True)
        out['klank:' + g] = base64.b64encode(open(mp3, 'rb').read()).decode()
    for i, (key, text) in enumerate(phrases.items()):
        wav, mp3 = os.path.join(tmp, f'{i}.wav'), os.path.join(tmp, f'{i}.mp3')
        subprocess.run([piper, '--model', model, '--output_file', wav, '--length_scale', '1.12', '--sentence_silence', '0'],
                       input=text.encode(), check=True, capture_output=True)
        # trim silence at both ends, mono 22 kHz 40 kbps
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af',
                        'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.08',
                        '-ac', '1', '-ar', '22050', '-b:a', '40k', mp3], check=True)
        out[key] = base64.b64encode(open(mp3, 'rb').read()).decode()
json.dump(out, open(os.path.join(root, 'voice.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
print(len(out), 'phrases')
