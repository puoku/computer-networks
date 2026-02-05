from icmplib import ping
import csv

hosts = ["google.com", "youtube.com", "wikipedia.org", "openai.com","github.com",
        "store.steampowered.com", "apple.com", "wildberries.com", "ozon.com", "yandex.ru"]

filename = "results.csv"

with open(filename, "w", encoding="utf-8", newline = "") as csvfile:
    csv.writer(csvfile, dialect="excel").writerow(["Domain", "Is Alive", "Average RTT (ms)", "Packet Loss (%)", "Jitter (ms)"])
    for i in hosts:
        result = ping(i, count=10, timeout=2, interval=0.2, privileged=False)
        csv.writer(csvfile, dialect="excel").writerow([i, result.is_alive, result.avg_rtt, result.packet_loss, result.max_rtt - result.min_rtt])
print(filename, "сохранен")