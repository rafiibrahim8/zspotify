import requests
from librespot.core import Session
from librespot.metadata import TrackId

EMPTY: dict = {'lyrics': None, 'uslt': None, 'sylt': None, 'lang': None}

# ISO 639-1 (2-letter) -> ISO 639-2/B (3-letter) for the ID3 USLT/SYLT lang field.
# Bibliographic codes; same set ID3v2 examples use (ger, fre, dut, etc.).
ISO_639_1_TO_2 = {
    'aa': 'aar',
    'ab': 'abk',
    'ae': 'ave',
    'af': 'afr',
    'ak': 'aka',
    'am': 'amh',
    'an': 'arg',
    'ar': 'ara',
    'as': 'asm',
    'av': 'ava',
    'ay': 'aym',
    'az': 'aze',
    'ba': 'bak',
    'be': 'bel',
    'bg': 'bul',
    'bh': 'bih',
    'bi': 'bis',
    'bm': 'bam',
    'bn': 'ben',
    'bo': 'tib',
    'br': 'bre',
    'bs': 'bos',
    'ca': 'cat',
    'ce': 'che',
    'ch': 'cha',
    'co': 'cos',
    'cr': 'cre',
    'cs': 'cze',
    'cu': 'chu',
    'cv': 'chv',
    'cy': 'wel',
    'da': 'dan',
    'de': 'ger',
    'dv': 'div',
    'dz': 'dzo',
    'ee': 'ewe',
    'el': 'gre',
    'en': 'eng',
    'eo': 'epo',
    'es': 'spa',
    'et': 'est',
    'eu': 'baq',
    'fa': 'per',
    'ff': 'ful',
    'fi': 'fin',
    'fj': 'fij',
    'fo': 'fao',
    'fr': 'fre',
    'fy': 'fry',
    'ga': 'gle',
    'gd': 'gla',
    'gl': 'glg',
    'gn': 'grn',
    'gu': 'guj',
    'gv': 'glv',
    'ha': 'hau',
    'he': 'heb',
    'hi': 'hin',
    'ho': 'hmo',
    'hr': 'hrv',
    'ht': 'hat',
    'hu': 'hun',
    'hy': 'arm',
    'hz': 'her',
    'ia': 'ina',
    'id': 'ind',
    'ie': 'ile',
    'ig': 'ibo',
    'ii': 'iii',
    'ik': 'ipk',
    'io': 'ido',
    'is': 'ice',
    'it': 'ita',
    'iu': 'iku',
    'ja': 'jpn',
    'jv': 'jav',
    'ka': 'geo',
    'kg': 'kon',
    'ki': 'kik',
    'kj': 'kua',
    'kk': 'kaz',
    'kl': 'kal',
    'km': 'khm',
    'kn': 'kan',
    'ko': 'kor',
    'kr': 'kau',
    'ks': 'kas',
    'ku': 'kur',
    'kv': 'kom',
    'kw': 'cor',
    'ky': 'kir',
    'la': 'lat',
    'lb': 'ltz',
    'lg': 'lug',
    'li': 'lim',
    'ln': 'lin',
    'lo': 'lao',
    'lt': 'lit',
    'lu': 'lub',
    'lv': 'lav',
    'mg': 'mlg',
    'mh': 'mah',
    'mi': 'mao',
    'mk': 'mac',
    'ml': 'mal',
    'mn': 'mon',
    'mr': 'mar',
    'ms': 'may',
    'mt': 'mlt',
    'my': 'bur',
    'na': 'nau',
    'nb': 'nob',
    'nd': 'nde',
    'ne': 'nep',
    'ng': 'ndo',
    'nl': 'dut',
    'nn': 'nno',
    'no': 'nor',
    'nr': 'nbl',
    'nv': 'nav',
    'ny': 'nya',
    'oc': 'oci',
    'oj': 'oji',
    'om': 'orm',
    'or': 'ori',
    'os': 'oss',
    'pa': 'pan',
    'pi': 'pli',
    'pl': 'pol',
    'ps': 'pus',
    'pt': 'por',
    'qu': 'que',
    'rm': 'roh',
    'rn': 'run',
    'ro': 'rum',
    'ru': 'rus',
    'rw': 'kin',
    'sa': 'san',
    'sc': 'srd',
    'sd': 'snd',
    'se': 'sme',
    'sg': 'sag',
    'si': 'sin',
    'sk': 'slo',
    'sl': 'slv',
    'sm': 'smo',
    'sn': 'sna',
    'so': 'som',
    'sq': 'alb',
    'sr': 'srp',
    'ss': 'ssw',
    'st': 'sot',
    'su': 'sun',
    'sv': 'swe',
    'sw': 'swa',
    'ta': 'tam',
    'te': 'tel',
    'tg': 'tgk',
    'th': 'tha',
    'ti': 'tir',
    'tk': 'tuk',
    'tl': 'tgl',
    'tn': 'tsn',
    'to': 'ton',
    'tr': 'tur',
    'ts': 'tso',
    'tt': 'tat',
    'tw': 'twi',
    'ty': 'tah',
    'ug': 'uig',
    'uk': 'ukr',
    'ur': 'urd',
    'uz': 'uzb',
    've': 'ven',
    'vi': 'vie',
    'vo': 'vol',
    'wa': 'wln',
    'wo': 'wol',
    'xh': 'xho',
    'yi': 'yid',
    'yo': 'yor',
    'za': 'zha',
    'zh': 'chi',
    'zu': 'zul',
}


def _to_iso_639_2(code: str | None) -> str:
    if not code:
        return 'eng'
    return ISO_639_1_TO_2.get(code.lower(), 'eng')


def _unsynced_text(spotify_lyrics: dict) -> str:
    lines = [line.get('words', '') for line in spotify_lyrics['lyrics'].get('lines', [])]
    return '\n'.join(lines) + '\n'


def _lrc_text(spotify_lyrics: dict) -> str:
    lines = []
    for line in spotify_lyrics['lyrics'].get('lines', []):
        ts_ms = int(line.get('startTimeMs', 0))
        minutes = ts_ms // 60_000
        seconds = (ts_ms // 1000) % 60
        centis = (ts_ms % 1000) // 10
        text = line.get('words', '')
        lines.append(f'[{minutes:02d}:{seconds:02d}.{centis:02d}]{text}')
    return '\n'.join(lines) + '\n'


def _sylt_pairs(spotify_lyrics: dict) -> list[tuple[str, int]]:
    return [
        (line.get('words', ''), int(line.get('startTimeMs', 0)))
        for line in spotify_lyrics['lyrics'].get('lines', [])
    ]


def get_lyrics(track_id: str, session: Session) -> dict:
    """Fetch lyrics for a track.

    Returns a dict with four keys:
      - 'lyrics': str | None — plain text (unsynced) or LRC-formatted string (synced)
      - 'uslt':   str | None — text suitable for the ID3 USLT frame, only when unsynced
      - 'sylt':   list[(str, int)] | None — (line, ms) pairs for the ID3 SYLT frame, only when synced
      - 'lang':   str — ISO 639-2/B 3-letter code, ready for ID3 USLT/SYLT (defaults to 'eng')
    """
    tid = (
        TrackId.from_uri(track_id)
        if track_id.startswith('spotify:track:')
        else TrackId.from_base62(track_id)
    )
    b62 = tid.to_spotify_uri().split(':')[-1]

    headers = {
        'authorization': f'Bearer {session.tokens().get("user-read-email")}',
        'app-platform': 'WebPlayer',
        'user-agent': 'curl/8.20.0',  # Python's default UA gets rejected ¯\_(ツ)_/¯
    }
    params = {'format': 'json', 'vocalRemoval': 'false', 'market': 'from_token'}
    response = requests.get(
        f'https://spclient.wg.spotify.com/color-lyrics/v2/track/{b62}',
        headers=headers,
        params=params,
        timeout=30,
    )
    if response.status_code == 404:
        return dict(EMPTY)

    response.raise_for_status()
    spotify_lyrics = response.json()
    sync_type = spotify_lyrics['lyrics']['syncType']

    if sync_type == 'NOT_FOUND':
        return dict(EMPTY)
    lang = _to_iso_639_2(spotify_lyrics['lyrics'].get('language'))
    if sync_type == 'UNSYNCED':
        text = _unsynced_text(spotify_lyrics)
        return {'lyrics': text, 'uslt': text, 'sylt': None, 'lang': lang}
    if sync_type == 'LINE_SYNCED':
        return {
            'lyrics': _lrc_text(spotify_lyrics),
            'uslt': None,
            'sylt': _sylt_pairs(spotify_lyrics),
            'lang': lang,
        }
    raise ValueError(f'Unknown sync type: {sync_type}')
