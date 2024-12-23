import random
import csv

# Definisi hero dan peluangnya
heroes = {
    "Rare_A": 0.01, "Rare_B": 0.005, "Rare_C": 0.007, "Rare_D": 0.008, "Rare_E": 0.006,
    "Common_A": 0.15, "Common_B": 0.2, "Common_C": 0.18, "Common_D": 0.22, "Common_E": 0.2
}

# Fungsi untuk simulasi gacha
def pull_gacha(rate_up_hero=None, rate_up_bonus=0.01):
    """
    Simulasi 1 kali pull gacha.
    :param rate_up_hero: Hero rare yang mendapatkan bonus rate up.
    :param rate_up_bonus: Bonus peluang untuk hero rate up.
    :return: Hero yang didapat.
    """
    adjusted_heroes = heroes.copy()

    # Adjust peluang untuk rate up hero jika ada
    if rate_up_hero and rate_up_hero in adjusted_heroes:
        adjusted_heroes[rate_up_hero] += rate_up_bonus

    # Normalisasi peluang jika ada rate up
    total_probability = sum(adjusted_heroes.values())
    for hero in adjusted_heroes:
        adjusted_heroes[hero] /= total_probability

    # Pilih hero berdasarkan peluang
    choices, probabilities = zip(*adjusted_heroes.items())
    return random.choices(choices, probabilities)[0]

# Simulasi 5 hari dengan 100 user, 2 pull per hari
num_users = 100
pulls_per_user_per_day = 2
num_days = 5
rate_up_schedule = ["Rare_A", "Rare_B", "Rare_C", "Rare_D", "Rare_E"]

# Simpan hasil pull
results = {hero: 0 for hero in heroes}
user_data = {user: [] for user in range(1, num_users + 1)}

for day in range(1, num_days + 1):
    rate_up_hero = rate_up_schedule[day - 1]
    for user in range(1, num_users + 1):
        for _ in range(pulls_per_user_per_day):
            hero_pulled = pull_gacha(rate_up_hero=rate_up_hero)
            results[hero_pulled] += 1
            user_data[user].append(hero_pulled)

# Cetak hasil
print("Total pulls for each hero:")
for hero, count in results.items():
    print(f"{hero}: {count}")

# Analisis distribusi rare
rare_heroes = [hero for hero in heroes if "Rare" in hero]
rare_counts_per_user = [sum(1 for hero in user_data[user] if hero in rare_heroes) for user in user_data]

average_rare = sum(rare_counts_per_user) / num_users
std_dev_rare = (sum((x - average_rare) ** 2 for x in rare_counts_per_user) / num_users) ** 0.5

most_lucky_user = max(user_data, key=lambda u: sum(1 for h in user_data[u] if h in rare_heroes))
unluckiest_user = min(user_data, key=lambda u: sum(1 for h in user_data[u] if h in rare_heroes))

print("\nDistribusi rare:")
print(f"Rata-rata rare per user: {average_rare:.2f}")
print(f"Standar deviasi rare: {std_dev_rare:.2f}")
print(f"User paling beruntung: User {most_lucky_user}")
print(f"User paling ampas: User {unluckiest_user}")

# Simpan hasil dalam CSV
with open("gacha_results.csv", "w", newline="") as file:
    writer = csv.writer(file)

    # Header
    header = ["User"] + [f"Day {day} Pull {pull}" for day in range(1, num_days + 1) for pull in range(1, pulls_per_user_per_day + 1)]
    writer.writerow(header)

    # Data tiap user
    for user, pulls in user_data.items():
        row = [user] + pulls
        writer.writerow(row)

print("Hasil gacha disimpan dalam 'gacha_results.csv'")
