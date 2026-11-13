import yt_dlp

url = input("Insert a link to the video: ").strip()

with yt_dlp.YoutubeDL({}) as ydl:
    info = ydl.extract_info(url, download=False)

seen = set()
menu = []

for f in info['formats']:
    if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
        h = f.get('height')
        if h and h not in seen:
            seen.add(h)
            menu.append({
                'label': f"{h}p  (video only, will be merged with the audio)",
                'selector': f"bestvideo[height<={h}]+bestaudio/best",
            })

menu.append({
    'label': "audio only (best audio, m4a)",
    'selector': "bestaudio/best",
})

print("\nAvailable options:")
for i, item in enumerate(menu, start=1):
    print(f"  [{i}] {item['label']}")

while True:
    raw = input("\nEnter the option number: ").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(menu):
        choice = menu[int(raw) - 1]
        break
    print("That number doesn't exist. Try again.")

print(f"\nSelected: {choice['label']}")
print("Download...\n")

opts = {
    'format': choice['selector'],
    'outtmpl': "%(title)s.%(ext)s",
    "merge_output_format": 'mp4',
}

with yt_dlp.YoutubeDL(opts) as ydl:
    ydl.download([url])

print("\nDone!")