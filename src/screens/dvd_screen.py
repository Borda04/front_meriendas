import flet as ft
import asyncio
import random

def crear_fondo_dvd(page: ft.Page):
    logo_size = 100
    # List of image paths from the 'aset' folder
    image_paths = [f"foto{i}.png" for i in range(1, 10)]
    current_image_index = random.randint(0, len(image_paths) - 1)

    logo_image = ft.Image(
        src=image_paths[current_image_index],
        width=logo_size,
        height=logo_size,
        fit=ft.ImageFit.CONTAIN,
    )

    logo = ft.Container(
        width=logo_size,
        height=logo_size,
        content=logo_image,  # Set the image as content
        border_radius=5,
    )

    x_pos = random.randint(0, int(page.width) - logo_size)
    y_pos = random.randint(0, int(page.height) - logo_size)
    vx = 2
    vy = 2

    async def animate():
        nonlocal x_pos, y_pos, vx, vy, current_image_index

        while True:
            x_pos += vx
            y_pos += vy

            # Check for wall collision
            wall_hit = False
            if x_pos + logo_size >= page.width or x_pos <= 0:
                vx = -vx
                wall_hit = True

            if y_pos + logo_size >= page.height or y_pos <= 0:
                vy = -vy
                wall_hit = True

            if wall_hit:
                # Change image on any wall hit
                new_index = random.randint(0, len(image_paths) - 1)
                while new_index == current_image_index: # Ensure a different image is picked
                    new_index = random.randint(0, len(image_paths) - 1)
                current_image_index = new_index
                logo_image.src = image_paths[current_image_index]

                

            logo.left = x_pos
            logo.top = y_pos
            page.update()
            await asyncio.sleep(0.01)

    

    dvd_stack = ft.Stack(
        [
            logo
        ],
        width=page.width,
        height=page.height
    )

    page.run_task(animate)

    return dvd_stack