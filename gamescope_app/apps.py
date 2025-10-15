from django.apps import AppConfig
from django.contrib.auth import get_user_model
from datetime import date

class GamescopeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gamescope_app'

    def ready(self):
        from django.conf import settings
        User = get_user_model()
        
        # Import models here to avoid AppRegistryNotReady
        from .models import Game

        # --- Create superuser if it doesn't exist ---
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="StrongPassword123"
            )
            print("Superuser created!")

        # --- Add 45 games if they don't exist ---
        if not Game.objects.exists():
            games = [
            {"name": "The Legend of Zelda: Tears of the Kingdom", "description": "Open-world adventure with puzzles and dungeons.", "genre": "Action-Adventure", "number_of_players": 1, "platform": "Switch", "release_date": date(2023,5,12)},
            {"name": "Hades II", "description": "Sequel to Hades, roguelike with deep narrative.", "genre": "Roguelike", "number_of_players": 1, "platform": "PC, Switch", "release_date": date(2025,11,20)},
            {"name": "Monster Hunter World", "description": "Hunt massive monsters in a vast world.", "genre": "Action RPG", "number_of_players": 4, "platform": "PC/PS4/Xbox", "release_date": date(2018,1,26)},
            {"name": "Elden Ring", "description": "Open-world dark fantasy RPG.", "genre": "RPG", "number_of_players": 1, "platform": "PC/PS4/PS5/Xbox", "release_date": date(2022,2,25)},
            {"name": "God of War Ragnarok", "description": "Kratos continues his journey in Norse mythology.", "genre": "Action-Adventure", "number_of_players": 1, "platform": "PS4/PS5", "release_date": date(2022,11,9)},
            {"name": "Cyberpunk 2077", "description": "Futuristic RPG in Night City.", "genre": "RPG", "number_of_players": 1, "platform": "PC/PS4/PS5/Xbox", "release_date": date(2020,12,10)},
            {"name": "Halo Infinite", "description": "Master Chief returns in a new Halo adventure.", "genre": "Shooter", "number_of_players": 16, "platform": "PC/Xbox", "release_date": date(2021,12,8)},
            {"name": "Minecraft", "description": "Build and explore infinite worlds.", "genre": "Sandbox", "number_of_players": 8, "platform": "PC/Consoles/Mobile", "release_date": date(2011,11,18)},
            {"name": "Fortnite", "description": "Battle Royale and creative mode fun.", "genre": "Battle Royale", "number_of_players": 100, "platform": "PC/Consoles/Mobile", "release_date": date(2017,7,21)},
            {"name": "Among Us", "description": "Social deduction multiplayer game.", "genre": "Party", "number_of_players": 10, "platform": "PC/Mobile/Console", "release_date": date(2018,6,15)},
            {"name": "The Witcher 3: Wild Hunt", "description": "Open-world fantasy RPG with monsters and magic.", "genre": "RPG", "number_of_players": 1, "platform": "PC/PS4/Xbox/Switch", "release_date": date(2015,5,19)},
            {"name": "Grand Theft Auto V", "description": "Open-world crime adventure.", "genre": "Action-Adventure", "number_of_players": 30, "platform": "PC/PS4/PS5/Xbox", "release_date": date(2013,9,17)},
            {"name": "Red Dead Redemption 2", "description": "Western-themed open-world adventure.", "genre": "Action-Adventure", "number_of_players": 1, "platform": "PC/PS4/Xbox", "release_date": date(2018,10,26)},
            {"name": "Call of Duty: Modern Warfare II", "description": "FPS with multiplayer and campaign modes.", "genre": "Shooter", "number_of_players": 20, "platform": "PC/PS4/PS5/Xbox", "release_date": date(2022,10,28)},
            {"name": "Overwatch 2", "description": "Team-based hero shooter.", "genre": "Shooter", "number_of_players": 12, "platform": "PC/PS4/PS5/Xbox/Switch", "release_date": date(2022,10,4)},
            {"name": "FIFA 23", "description": "Soccer simulation game.", "genre": "Sports", "number_of_players": 4, "platform": "PC/PS4/PS5/Xbox", "release_date": date(2022,9,30)},
            {"name": "NBA 2K23", "description": "Basketball simulation game.", "genre": "Sports", "number_of_players": 4, "platform": "PC/PS4/PS5/Xbox", "release_date": date(2022,9,9)},
            {"name": "Pokemon Scarlet", "description": "Open-world Pokémon adventure.", "genre": "RPG", "number_of_players": 2, "platform": "Switch", "release_date": date(2022,11,18)},
            {"name": "Pokemon Violet", "description": "Companion game to Scarlet.", "genre": "RPG", "number_of_players": 2, "platform": "Switch", "release_date": date(2022,11,18)},
            {"name": "Animal Crossing: New Horizons", "description": "Life simulation and village building.", "genre": "Simulation", "number_of_players": 8, "platform": "Switch", "release_date": date(2020,3,20)},
            {"name": "Super Mario Odyssey", "description": "3D platformer adventure with Mario.", "genre": "Platformer", "number_of_players": 2, "platform": "Switch", "release_date": date(2017,10,27)},
            {"name": "Mario Kart 8 Deluxe", "description": "Fun racing game with iconic Nintendo characters.", "genre": "Racing", "number_of_players": 8, "platform": "Switch", "release_date": date(2017,4,28)},
            {"name": "Luigi’s Mansion 3", "description": "Puzzle-adventure in a haunted hotel.", "genre": "Action-Adventure", "number_of_players": 2, "platform": "Switch", "release_date": date(2019,10,31)},
            {"name": "Splatoon 3", "description": "Colorful team-based shooter.", "genre": "Shooter", "number_of_players": 8, "platform": "Switch", "release_date": date(2022,9,9)},
            {"name": "Metroid Dread", "description": "Side-scrolling action-adventure.", "genre": "Action-Adventure", "number_of_players": 1, "platform": "Switch", "release_date": date(2021,10,8)},
            {"name": "Hollow Knight: Silksong", "description": "Sequel to the acclaimed Hollow Knight.", "genre": "Metroidvania", "number_of_players": 1, "platform": "PC/Consoles", "release_date": date(2025,3,1)},
            {"name": "Stardew Valley", "description": "Farming and life simulator.", "genre": "Simulation", "number_of_players": 4, "platform": "PC/Consoles/Mobile", "release_date": date(2016,2,26)},
            {"name": "Terraria", "description": "2D sandbox adventure.", "genre": "Sandbox", "number_of_players": 8, "platform": "PC/Consoles/Mobile", "release_date": date(2011,5,16)},
            {"name": "The Sims 4", "description": "Life simulation game.", "genre": "Simulation", "number_of_players": 4, "platform": "PC/Consoles", "release_date": date(2014,9,2)},
            {"name": "League of Legends", "description": "MOBA online multiplayer.", "genre": "MOBA", "number_of_players": 10, "platform": "PC", "release_date": date(2009,10,27)},
            {"name": "Dota 2", "description": "MOBA with global esports scene.", "genre": "MOBA", "number_of_players": 10, "platform": "PC", "release_date": date(2013,7,9)},
            {"name": "Valorant", "description": "Tactical team-based shooter.", "genre": "Shooter", "number_of_players": 10, "platform": "PC", "release_date": date(2020,6,2)},
            {"name": "Apex Legends", "description": "Battle Royale with unique characters.", "genre": "Battle Royale", "number_of_players": 60, "platform": "PC/PS4/PS5/Xbox/Switch", "release_date": date(2019,2,4)},
            {"name": "Rust", "description": "Multiplayer survival game.", "genre": "Survival", "number_of_players": 100, "platform": "PC/Consoles", "release_date": date(2018,2,8)},
            {"name": "ARK: Survival Evolved", "description": "Survive in a world with dinosaurs.", "genre": "Survival", "number_of_players": 100, "platform": "PC/Consoles", "release_date": date(2017,8,29)},
            {"name": "The Elder Scrolls V: Skyrim", "description": "Open-world fantasy RPG.", "genre": "RPG", "number_of_players": 1, "platform": "PC/Consoles", "release_date": date(2011,11,11)},
            {"name": "Fall Guys: Ultimate Knockout", "description": "Battle Royale party game.", "genre": "Party", "number_of_players": 60, "platform": "PC/Consoles", "release_date": date(2020,8,4)},
            {"name": "Cuphead", "description": "Run-and-gun platformer with 1930s cartoon art.", "genre": "Platformer", "number_of_players": 2, "platform": "PC/Consoles", "release_date": date(2017,9,29)},
            {"name": "Celeste", "description": "Challenging platformer about climbing a mountain.", "genre": "Platformer", "number_of_players": 1, "platform": "PC/Consoles", "release_date": date(2018,1,25)},
            {"name": "Dead Cells", "description": "Roguelike Metroidvania with procedurally-generated levels.", "genre": "Roguelike", "number_of_players": 1, "platform": "PC/Consoles/Mobile", "release_date": date(2018,8,7)},
            {"name": "Slay the Spire", "description": "Deck-building roguelike game.", "genre": "Roguelike", "number_of_players": 1, "platform": "PC/Consoles/Mobile", "release_date": date(2019,1,23)},
            {"name": "Ori and the Will of the Wisps", "description": "Beautiful Metroidvania platformer.", "genre": "Platformer", "number_of_players": 1, "platform": "PC/Xbox/Consoles", "release_date": date(2020,3,11)},
            {"name": "Resident Evil Village", "description": "Survival horror game.", "genre": "Horror", "number_of_players": 1, "platform": "PC/PS4/PS5/Xbox", "release_date": date(2021,5,7)},
            ]

            for game_data in games:
                Game.objects.create(**game_data)

            print("45 games added successfully!")
