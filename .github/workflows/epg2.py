from datetime import datetime, timedelta, timezone
import json
import xml.etree.ElementTree as ET
import requests

API_URL = 'https://now.truevisions.co.th/api/video/live-schedules'

HEADERS = {
    'Content-Type': 'application/json',
    'Origin': 'https://now.truevisions.co.th',
    'Referer': 'https://now.truevisions.co.th/th/channel?tab=schedule',
    'User-Agent': (
        'Mozilla/5.0 (Linux; Android 16; Pixel 10) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/155.0.0.0 Mobile Safari/537.36'
    ),
    'X-Device-Id': 'chrome-1791804520413',
    'X-User-Lang': 'th',
    'X-User-Rate': 'adult',
    'Accept': 'application/json, text/plain, */*',
}

TZ = timezone(timedelta(hours=7))
DATE_FMT = '%Y-%m-%d'

CHANNELS = [
    # ทีวีดิจิทัล
    {'id': 'tnn16', 'name': 'TNN16', 'content_id': '57Zw61l0vOxk'},  
    {'id': 'true4u', 'name': 'True4U', 'content_id': '5zAEqWKW358z'},  
    {'id': 'ch3hd', 'name': 'CH3 HD', 'content_id': 'VldbdQ2VqwoY'},  
    {'id': 'ch5', 'name': 'CH5', 'content_id': '2X0yGL8lKKQA'},  
    {'id': 'ch7hd', 'name': 'CH7 HD', 'content_id': '9O54lyP5Rqx'},  
    {'id': 'mcothd', 'name': 'MCOT HD', 'content_id': '512vaBKOAlM1'},  
    {'id': 'nbt', 'name': 'NBT', 'content_id': 'PVq6XgWy8X4w'},  
    {'id': 'thaipbs', 'name': 'Thai PBS', 'content_id': '2EqxWv4RYdBy'},  
    {'id': 'thairathhd', 'name': 'Thairath HD', 'content_id': '0VW70g35rNgV'},  
    {'id': 'onehd', 'name': 'ONE HD', 'content_id': 'BejNOdZGL4Me'},  
    {'id': 'ch8', 'name': 'CH8', 'content_id': 'M8OropBYrbVa'},  
    {'id': 'gmm25', 'name': 'GMM25', 'content_id': '5mZpVxW12gaE'},  
    {'id': 'nation', 'name': 'Nation', 'content_id': 'O3aAl47MR2M3'},  
    {'id': 'workpoint', 'name': 'Workpoint', 'content_id': 'jyrKPQXGd5b7'},  
    {'id': 'amarinhd', 'name': 'Amarin HD', 'content_id': 'Zer69qrrVLWe'},  
    {'id': 'ppvhd', 'name': 'PPTV HD', 'content_id': '5aWqbJMQeDvy'},  
    {'id': 'tsports', 'name': 'T-Sports', 'content_id': 'YkmmYPRvOEyk'},  
    # ฟรีทีวี
    {'id': 'tnn2', 'name': 'TNN2', 'content_id': 'E9k68z9aKDp'},  
    {
        'id': 'ramachannel',
        'name': 'Rama Channel',
        'content_id': 'r71LNbqjaKe',
    },  
    {
        'id': 'trueplookpanya',
        'name': 'ทรู ปลูกปัญญา',
        'content_id': '9WmoQMj0NOp',
    },  
    {
        'id': 'platgoldhighlight',
        'name': 'Plat&Gold Highlight',
        'content_id': 'Rg0xJd9Wmj9g',
    },  
    {'id': 'motogp2', 'name': 'MotoGP 2', 'content_id': 'VkGzpXZj6vxQ'},  
    {'id': 'fifaplus', 'name': 'FIFA+', 'content_id': 'AOqrdxzx6nAB'},  
    # ภาพยนตร์และซีรีส์
    {
        'id': 'truemovieshits',
        'name': 'True Movies Hits',
        'content_id': 'NopZ5gjkGmE',
    },  
    {
        'id': 'trueasianmore',
        'name': 'True Asian More',
        'content_id': 'A36nrdXGn3V',
    },  
    {
        'id': 'truethaifilm',
        'name': 'True Thai Film',
        'content_id': 'GNd67OBJ6pv',
    },  
    {
        'id': 'kbsworldhd',
        'name': 'KBS World HD',
        'content_id': 'J2LMzNN8k4K',
    },  
    {'id': 'truefilm1', 'name': 'True Film 1', 'content_id': 'PanRBOzKovQ'},  
    {'id': 'rockaction', 'name': 'Rock Action', 'content_id': '3AqanG58Er3'},  
    {'id': 'truefilm2', 'name': 'True Film 2', 'content_id': '4QmJ09AyPm4'},  
    {'id': 'ccm', 'name': 'CCM', 'content_id': 'B9alY9gp0vB'},  
    {
        'id': 'truefilmasia',
        'name': 'True Film Asia',
        'content_id': 'mXQoNYKda2L9',
    },  
    {
        'id': 'rockxstream',
        'name': 'Rock X Stream',
        'content_id': 'x0lxY8Qmgrw0',
    },  
    {'id': 'iqiyi', 'name': 'iQIYI', 'content_id': 'dZ7OeBX2YYRZ'},  
    {'id': 'tvnasia', 'name': 'tvN Asia', 'content_id': 'x0M8Vnxxjgab'},  
    # บันเทิง
    {
        'id': 'truexzyte',
        'name': 'True X-Zyte',
        'content_id': 'jqepWV3ka8j',
    },  
    {
        'id': 'truelittlemonk',
        'name': 'True Little Monk Reality',
        'content_id': '9xQq7Yk7Jzr',
    },  
    {
        'id': 'rockentertainment',
        'name': 'Rock Entertainment',
        'content_id': 'nbyAVeb1jpN',
    },  
    {
        'id': 'fashiontvhd',
        'name': 'Fashion TV HD',
        'content_id': 'DpZV0741AWz',
    },  
    {'id': 'axnhd', 'name': 'AXN HD', 'content_id': 'n8OW8d0x0qA'},  
    {
        'id': 'bbclifestyle',
        'name': 'BBC Lifestyle',
        'content_id': 'xkZ7M890k1z',
    },  
    {'id': 'dwenglish', 'name': 'DW English', 'content_id': 'RVrAxAOGx21v'},  
    {'id': 'arirang', 'name': 'Arirang', 'content_id': 'gqVn9n7MeYXq'},  
    {'id': 'soulsiam', 'name': 'Soul Siam', 'content_id': 'ANpeVzyVVAw1'},  
    {'id': 'afreality', 'name': 'AF Reality', 'content_id': 'J6zPvDYrYegw'},  
    # เด็ก
    {
        'id': 'truesparkplay',
        'name': 'True Spark Play',
        'content_id': 'P83vkq1M1Lp',
    },  
    {
        'id': 'cartoonnetwork',
        'name': 'Cartoon Network',
        'content_id': 'bN8M16MRd20',
    },  
    {'id': 'nickjr', 'name': 'Nick Jr', 'content_id': 'mJVNNe2vdbBJ'},  
    {'id': 'dreamworks', 'name': 'Dreamworks', 'content_id': '3ELoobaOBdd9'},  
    # สาระความรู้
    {
        'id': 'discoverychannel',
        'name': 'Discovery Channel',
        'content_id': 'dQ9rmrAZjrXv',
    },  
    {
        'id': 'trueexplorewild',
        'name': 'True Explore Wild',
        'content_id': 'vNG2L371k5W',
    },  
    {
        'id': 'trueexploresci',
        'name': 'True Explore Sci',
        'content_id': 'mVoXV1rk4B5',
    },  
    {
        'id': 'discoveryasia',
        'name': 'Discovery Asia',
        'content_id': 'rODK2KQqNyoM',
    },  
    {
        'id': 'historychannel',
        'name': 'History Channel HD',
        'content_id': 'OX4KG1R3W8O',
    },  
    # กีฬา
    {'id': 'truetennis', 'name': 'True Tennis', 'content_id': 'Q7vaEm8O9e4'},  
    {'id': 'truesport5', 'name': 'True Sport 5', 'content_id': 'zmvD0RO72nL'},  
    {'id': 'truesport4', 'name': 'True Sport 4', 'content_id': 'GDna51EdVk4'},  
    {'id': 'truesport1', 'name': 'True Sport 1', 'content_id': 'wQZrKd3mo65'},  
    {'id': 'truesport7', 'name': 'True Sport 7', 'content_id': 'GPVMYwpnzKv'},  
    {
        'id': 'beinsports1f1',
        'name': 'beIN SPORTS 1 (F1)',
        'content_id': 'g9ONWXWJV5pq',
    },  
    {'id': 'beinsports3', 'name': 'beIN SPORTS 3', 'content_id': '3wLvyKyryPAD'},  
    {'id': 'beinsports6', 'name': 'beIN SPORTS 6', 'content_id': '3JYow6Dx7zx0'},  
    {'id': 'beinsports4', 'name': 'beIN SPORTS 4', 'content_id': 'eyEPa8A2WaJN'},  
    {'id': 'beinsports5', 'name': 'beIN SPORTS 5', 'content_id': 'pQNm6nA20a6e'},  
    {
        'id': 'truepremierfootball3',
        'name': 'True Premier Football 3',
        'content_id': 'GdgqaeMewGp4',
    },  
    {
        'id': 'truepremierfootball4',
        'name': 'True Premier Football 4',
        'content_id': 'zyab4aWZ0OWx',
    },  
    {
        'id': 'truepremierfootball5',
        'name': 'True Premier Football 5',
        'content_id': 'pmXrb1NjLeP0',
    },  
    {'id': 'truesport2', 'name': 'True Sport 2', 'content_id': 'xR0n6ePG7wL'},  
    {'id': 'truesport3', 'name': 'True Sport 3', 'content_id': 'KEN52vz3o6M'},  
    {'id': 'spotv1', 'name': 'SPOTV1', 'content_id': 'bDKPPGOdyAmn'},  
    {'id': 'spotv2', 'name': 'SPOTV2', 'content_id': '2L1ZZdJGxPej'},  
    {'id': 'beinsports2', 'name': 'beIN SPORTS 2', 'content_id': '5XaDjQd1JJgw'},  
    {'id': 'motogp1', 'name': 'MotoGP 1', 'content_id': '7BRZKqNv1opB'},  
    {'id': 'beinsports1', 'name': 'beIN SPORTS 1', 'content_id': '2Yyb9xXEgeOJ'},  
    {'id': 'volleyball1', 'name': 'Volleyball 1', 'content_id': 'GDwwA11rPBgD'},  
    {'id': 'volleyball2', 'name': 'Volleyball 2', 'content_id': '4QGmlkkeqBd1'},  
    {'id': 'trueballthai1', 'name': 'True Ball Thai 1', 'content_id': 'Vwz1j7XVRkdn'},  
    # ข่าว
    {'id': 'cnnhd', 'name': 'CNN HD', 'content_id': 'vmDMJ9qmJxg'},  
    {'id': 'cctv4', 'name': 'CCTV4', 'content_id': 'xDYqbGEY4lK'},  
    {'id': 'tv5monde', 'name': 'TV5Monde', 'content_id': 'wkOEnAR062w'},  
    {
        'id': 'phoenixinfonews',
        'name': 'Phoenix InfoNews',
        'content_id': 'jbzlQpWG6nj',
    },  
    {
        'id': 'bbcworldnews',
        'name': 'BBC World News',
        'content_id': 'lQm56Ow0wjl',
    },  
    {
        'id': 'nhkworldpremium',
        'name': 'NHK World Premium',
        'content_id': 'ZDMz290leq8',
    },  
    {'id': 'nhkworldtv', 'name': 'NHK World TV', 'content_id': 'dyZWzDo7b0q'},  
    {'id': 'russiatoday', 'name': 'Russia Today', 'content_id': 'G91q58rrakG'},  
    {'id': 'cgtn', 'name': 'CGTN', 'content_id': '18bXErKy2Am'},  
    {'id': 'abcaustralia', 'name': 'ABC Australia', 'content_id': 'eM73Dj2x6pk'},  
    {'id': 'aljazeera', 'name': 'Aljazeera', 'content_id': 'MDDoq1pvaVM'},  
    {'id': 'cnbc', 'name': 'CNBC', 'content_id': 'NPDG7knzdgN'},  
]



def to_xmltv_time(value):
    """แปลงค่าเวลาให้เป็นรูปแบบ XMLTV: YYYYMMDDHHMMSS +HHMM"""
    if not value:
        return ''

    # Unix timestamp (วินาที หรือ มิลลิวินาที)
    if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
        ts = float(value)
        if ts > 1e12:
            ts /= 1000
        dt = datetime.fromtimestamp(ts, TZ)
        return dt.strftime('%Y%m%d%H%M%S %z')

    s = str(value).strip()

    # แทน Z ด้วย +00:00 สำหรับ fromisoformat
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'

    dt = None
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        # fallback ตัด milliseconds ออก (สำหรับ Python เก่าที่ fromisoformat ยังไม่รองรับ)
        import re
        s2 = re.sub(r'\.\d+', '', s)
        try:
            dt = datetime.fromisoformat(s2)
        except ValueError:
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%d/%m/%Y %H:%M:%S'):
                try:
                    dt = datetime.strptime(s2, fmt)
                    break
                except ValueError:
                    dt = None
            if dt is None:
                return ''

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ)
    else:
        dt = dt.astimezone(TZ)
    return dt.strftime('%Y%m%d%H%M%S %z')


def pick(d, *keys, default=''):
    for k in keys:
        if k in d and d[k] not in (None, ''):
            return d[k]
    return default


def extract_programs(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ('programs', 'programmes', 'data', 'items', 'results', 'schedules'):
            v = data.get(key)
            if isinstance(v, list):
                return v
            if isinstance(v, dict):
                for key2 in ('programs', 'programmes', 'items', 'results', 'schedules'):
                    v2 = v.get(key2)
                    if isinstance(v2, list):
                        return v2
    return []


def fetch_schedule(content_id, date_str):
    payload = {'contentId': content_id, 'date': date_str}
    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)
    print(f"   Status: {r.status_code}")
    r.raise_for_status()
    data = r.json()

    # DEBUG: แสดงโครงสร้าง JSON
    print("   Response preview:", json.dumps(data, ensure_ascii=False)[:500])

    return extract_programs(data)


# ---- คีย์เวลาที่รองรับ (จัดลำดับความสำคัญ) ----
START_KEYS = (
    'start_date',      # ← API truevisions ใช้คีย์นี้
    'startTime', 'start_time', 'startDateTime',
    'startDate', 'startAt', 'start',
    'beginTime', 'begin', 'from',
    'date',            # fallback สุดท้าย
)
STOP_KEYS = (
    'end_date',        # ← API truevisions ใช้คีย์นี้
    'endTime', 'end_time', 'endDateTime',
    'endDate', 'endAt', 'stop',
    'finishTime', 'finish', 'to',
)


def generate_epg_xml():
    tv = ET.Element('tv', {
        'generator-info-name': 'TrueVisions EPG Grabber by Python'
    })

    for ch in CHANNELS:
        c = ET.SubElement(tv, 'channel', {'id': ch['id']})
        ET.SubElement(c, 'display-name').text = ch['name']

    today = datetime.now(TZ).strftime(DATE_FMT)

    for ch in CHANNELS:
        print(f"กำลังดึง: {ch['name']} ({ch['content_id']})")
        try:
            programs = fetch_schedule(ch['content_id'], today)
        except Exception as e:
            print(f"   ERROR: {e}")
            continue

        if not programs:
            print("   ไม่พบรายการ")
            continue

        # DEBUG: ดูคีย์ของรายการแรก
        print("   Keys:", list(programs[0].keys()))

        count = 0
        for prog in programs:
            start_str = to_xmltv_time(pick(prog, *START_KEYS))
            stop_str = to_xmltv_time(pick(prog, *STOP_KEYS))

            # ถ้ามี start แต่ไม่มี stop → สมมติยาว 30 นาที
            if start_str and not stop_str:
                dt = datetime.strptime(start_str[:14], '%Y%m%d%H%M%S').replace(tzinfo=TZ)
                stop_str = (dt + timedelta(minutes=30)).strftime('%Y%m%d%H%M%S %z')

            if not start_str or not stop_str:
                print("   skip (no time):", pick(prog, 'title', 'name'))
                continue

            p = ET.SubElement(tv, 'programme', {
                'channel': ch['id'],
                'start': start_str,
                'stop': stop_str,
            })
            ET.SubElement(p, 'title').text = pick(
                prog, 'title', 'name', default='ไม่มีชื่อรายการ'
            )
            ET.SubElement(p, 'desc').text = pick(
                prog, 'description', 'synopsis', 'desc', default=''
            )
            count += 1

        print(f"   ✓ เพิ่ม {count} รายการ")

    ET.ElementTree(tv).write(
        'true_epg_complete.xml', encoding='utf-8', xml_declaration=True
    )
    print('\nบันทึก true_epg_complete.xml แล้ว')


if __name__ == '__main__':
    generate_epg_xml()