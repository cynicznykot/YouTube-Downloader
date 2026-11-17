from download import get_info, build_menu, download

url = input("Insert a link to the video: ").strip()

info = get_info(url)
menu = build_menu(info)

print("\nAvailable options:")
for i, item in enumerate(menu, start=1):
    print(f"   [{i}] {item['lable']}")

while True:
    raw = input("\nEnter the option number: ").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(menu):
        choice = menu[int(raw) - 1]
        break
    print("That number doesn't exist. Try again.")

print(f"\nSelected: {choice['label']}")

while True:
    container = input("Choose container (mp4/webm): ").strip().lower()
    if container in ('mp4', 'webm'):
        break
    print("Only mp4 or webm. Try again.")

folder = input("Save to folder (Enter = current folder): ").strip()
if not folder:
    folder = "."

print("Download...\n")
download(url, choice['selector'], folder, container)
print("\nDone!")