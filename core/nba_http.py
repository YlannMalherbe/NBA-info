"""En-têtes communs pour les requêtes vers le CDN public NBA."""

# Le CDN attend aussi les client hints et les métadonnées Fetch en HTTP/1.1.
# Source : https://github.com/sportsdataverse/hoopR/blob/main/R/utils_nba_stats.R
# Garder la version de Chrome cohérente entre User-Agent et sec-ch-ua.
HEADERS = {
    "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.nba.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.nba.com/",
    "Accept-Language": "en-US,en;q=0.9",
}
