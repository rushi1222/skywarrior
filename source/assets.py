# assets.py
import bullet
import clouds
import explosion
import fighter
import player
import minimap
import font  # Optional if you want to preload fonts as well
import requests
import io

def preload_all_assets():
    """
    Preloads (downloads and caches) every image or font you need from S3.
    Call this exactly once (e.g., before creating your Game() class or running the main loop).
    """
    # 1. BULLETS
    bullet.get_bullet_image()  
    # (This ensures bullet.py won't download the bullet image again later.)

    # 2. CLOUDS
    for i in range(1, 14):
        clouds.get_cloud_image(i)

    # 3. EXPLOSION FRAMES
    for i in range(1, 12):
        explosion.get_explosion_frame(i, size=0.75)

    # 4. FIGHTERS / EMP
    fighter.get_fighter_images()
    fighter.get_emp_images()

    # 5. PLAYER IMAGES
    #   (top, sonic, boom, damage, ship)
    for i in range(1, 7):
        player.get_player_top_image(i)
        player.get_sonic_image(i)
    for i in range(1, 9):
        player.get_boom_image(i)
    player.get_damage_image()
    player.get_ship_image()

    # 6. MINIMAP
    minimap.get_map_outline()

    # 7. (OPTIONAL) FONTS
    # If you want to preload the fonts so they won't re-download:
    font.get_karma_font(30)  # "BigFontSystem"
    font.get_karma_font(20)  # "SmallFontSystem"
    # ... or any additional sizes you might need

    print("All assets have been preloaded successfully!")
