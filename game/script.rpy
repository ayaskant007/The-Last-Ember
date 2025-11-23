# The Last Ember - Atmosphere Edition
# A game about sacrifice in a frozen world.

# Define characters
define e = Character("Elara", color="#c8ffc8")
define k = Character("Keeper", color="#ffcccc")

# --- Visual Effects (Code Based) ---

# Snow Effect using Text particles (since we can't generate images)
image snow_particle = Text("*", size=40, color="#ffffff88")
image snow_effect = SnowBlossom("snow_particle", count=50, border=50, xspeed=(20, 50), yspeed=(100, 150), start=0)

# Fire Flicker Effect
# Creates a semi-transparent orange overlay that pulses in opacity
image fire_overlay = Solid("#ff6600")

transform flicker_anim:
    alpha 0.1
    linear 0.1 alpha 0.15
    linear 0.1 alpha 0.05
    linear 0.2 alpha 0.12
    repeat

# Background Transforms
transform bg_fill:
    size (1920, 1080)
    fit "cover"

# Images
image bg wasteland = At("images/bg_frozen_wasteland.png", bg_fill)
image bg shelter = At("images/bg_shelter_interior.png", bg_fill)
image bg storage = At("images/bg_storage_room.png", bg_fill)
image bg entrance = At("images/bg_entrance_door.png", bg_fill)

image elara neutral = "images/elara_neutral.png"
image elara sad = "images/elara_sad.png"

# Game variables
default warmth = 60
default hope = 60
default day = 1
default max_days = 5  # Extended game length
default current_room = "main_hall"
default actions_taken = 0
default max_actions_per_day = 2

# --- Styles ---
style bar_warmth:
    right_bar Frame(Solid("#440000"), 0, 0)
    left_bar Frame(Solid("#ffaa00"), 0, 0)
    thumb None
    ysize 20

style bar_hope:
    right_bar Frame(Solid("#000044"), 0, 0)
    left_bar Frame(Solid("#8888ff"), 0, 0)
    thumb None
    ysize 20

# --- Screens ---

screen stats_overlay():
    frame:
        xalign 0.02
        yalign 0.02
        background "#000000aa"
        padding (20, 20)
        vbox:
            spacing 5
            text "Day [day]" size 40 color "#ffffff" bold True
            
            null height 15
            
            text "Warmth ([warmth]%)" color "#ffaa00" size 22
            bar value warmth range 100 xsize 300 style "bar_warmth"
            
            text "Hope ([hope]%)" color "#aaaaff" size 22
            bar value hope range 100 xsize 300 style "bar_hope"
            
            null height 15
            
            text "Energy: [max_actions_per_day - actions_taken] / [max_actions_per_day]" size 22 color "#cccccc"

screen exploration_ui():
    # Room Navigation
    frame:
        xalign 0.98
        yalign 0.98
        background "#000000aa"
        padding (20, 20)
        hbox:
            spacing 20
            textbutton "Main Hall" action [SetVariable("current_room", "main_hall"), Jump("update_scene")]
            textbutton "Storage" action [SetVariable("current_room", "storage"), Jump("update_scene")]
            textbutton "Entrance" action [SetVariable("current_room", "entrance"), Jump("update_scene")]

    # Room Actions
    frame:
        xalign 0.02
        yalign 0.85
        background "#000000aa"
        padding (20, 20)
        vbox:
            spacing 10
            if current_room == "main_hall":
                text "Main Hall" size 30 bold True color "#ffccaa"
                textbutton "Talk to Elara" action Jump("action_talk_elara")
                textbutton "Tend the Fire" action Jump("action_tend_fire")
            
            elif current_room == "storage":
                text "Storage Room" size 30 bold True color "#aaccff"
                textbutton "Search for Fuel" action Jump("action_search_fuel")
                textbutton "Read Old Books" action Jump("action_read_books")

            elif current_room == "entrance":
                text "Entrance" size 30 bold True color "#ffffff"
                textbutton "Check Outside" action Jump("action_check_outside")
                textbutton "Reinforce Door" action Jump("action_reinforce_door")
            
            null height 10
            textbutton "End Day (Rest)" action Jump("night_phase") text_color "#ffaaaa"

# --- Game Start ---

label start:
    $ warmth = 60
    $ hope = 60
    $ day = 1
    $ current_room = "main_hall"

    scene bg wasteland with fade
    show snow_effect

    "{color=#aaddff}The wind howls outside.{/color} A constant reminder of the world we lost."
    
    scene bg shelter with dissolve
    show fire_overlay at flicker_anim # Apply the fire lighting effect
    show screen stats_overlay with dissolve

    "I am the Keeper. It is my duty to keep the flame alive."

    show elara neutral at center with dissolve
    e "Keeper... we have survived another night."

    jump update_scene

label update_scene:
    # Logic to show the correct background based on room
    if current_room == "main_hall":
        scene bg shelter
        show fire_overlay at flicker_anim
        show elara neutral at center
    elif current_room == "storage":
        scene bg storage
        # No fire overlay in storage, it's cold
    elif current_room == "entrance":
        scene bg entrance
        # No fire overlay, maybe snow effect if door is cracked?
        # Let's keep it simple for now.

    # Show the UI
    call screen exploration_ui

# --- Actions ---

label action_talk_elara:
    $ actions_taken += 1
    scene bg shelter
    show fire_overlay at flicker_anim
    show elara neutral
    
    $ topic = renpy.random.choice(["dreams", "food", "past", "weather"])
    
    if topic == "dreams":
        e "I dreamt of a green field last night. It felt so real."
        $ hope += 5
        "She smiles faintly."
    elif topic == "food":
        e "I'm so hungry. Do we have anything left?"
        $ hope -= 5
        "I shake my head. Not yet."
    elif topic == "past":
        e "Do you remember the summer? The heat of the sun?"
        k "Vaguely. It feels like a lifetime ago."
    else:
        e "The wind sounds angry today."
    
    jump check_actions

label action_tend_fire:
    $ actions_taken += 1
    $ warmth += 10
    scene bg shelter
    show fire_overlay at flicker_anim
    "You carefully arrange the embers to maximize the heat."
    jump check_actions

label action_search_fuel:
    $ actions_taken += 1
    scene bg storage
    "You scour the empty shelves."
    $ roll = renpy.random.randint(1, 10)
    if roll > 6:
        "You found some old wooden crates! (Warmth +)"
        $ warmth += 15
    elif roll > 3:
        "You found a few scraps of paper."
        $ warmth += 5
    else:
        "Nothing but dust and ice."
    jump check_actions

label action_read_books:
    $ actions_taken += 1
    scene bg storage
    "You read a passage from an old encyclopedia."
    $ hope += 5
    "It reminds you that a world exists outside this frozen hell."
    jump check_actions

label action_check_outside:
    $ actions_taken += 1
    scene bg entrance
    show snow_effect
    "You look through the viewport."
    $ warmth -= 5
    "The cold seeps through the glass, but the view is breathtakingly deadly."
    jump check_actions

label action_reinforce_door:
    $ actions_taken += 1
    scene bg entrance
    "You stuff rags into the cracks of the blast door. (Warmth +)"
    $ warmth += 5
    jump check_actions

label check_actions:
    if actions_taken >= max_actions_per_day:
        "You are too tired to do anything else today."
        jump night_phase
    else:
        jump update_scene

# --- Night Phase ---

label night_phase:
    $ actions_taken = 0
    scene bg shelter
    show fire_overlay at flicker_anim
    show elara neutral

    "Night falls. The temperature plummets."
    "The fire is dying. We must feed it."

    # Random Night Event
    $ event_roll = renpy.random.randint(1, 3)
    if event_roll == 1:
        "A heavy chunk of snow falls from the roof, shaking the shelter."
    elif event_roll == 2:
        "You hear wolves howling in the distance."
        $ hope -= 5

    menu:
        "What should I sacrifice tonight?"

        "Burn Books (Sacrifice Knowledge)":
            $ warmth += 30
            $ hope -= 5
            "{color=#ff0000}The history of the world goes up in smoke.{/color}"

        "Burn Furniture (Sacrifice Comfort)":
            $ warmth += 30
            $ hope -= 10
            "{color=#ff0000}We sit on the cold floor, but the fire roars.{/color}"

        "Burn the Seed Stock (Sacrifice Future)" if day == 3:
            $ warmth += 50
            $ hope -= 20
            "{color=#ff0000}The promise of spring turns to ash.{/color}"

        "Scrape together scraps (Low Heat)" if warmth > 20:
            $ warmth += 10
            "It's not enough fuel, but it's all we can spare."

    # Nightly decay
    $ warmth -= 25 # Colder each night
    $ day += 1
    
    if day > max_days:
        jump ending_survival
    if warmth <= 0:
        jump ending_frozen
    if hope <= 0:
        jump ending_despair

    jump update_scene

# --- Endings ---

label ending_survival:
    scene bg wasteland with fade
    show snow_effect
    hide screen stats_overlay
    hide fire_overlay
    "{b}The sun rises on the final day.{/b}"
    "We are cold, hungry, and tired... but we are alive."
    "The storm has passed."
    "{size=50}GOOD ENDING{/size}"
    return

label ending_frozen:
    scene bg shelter with fade
    hide screen stats_overlay
    hide fire_overlay
    "The fire flickers and dies."
    "{color=#00ffff}The cold rushes in, claiming us instantly.{/color}"
    "{size=50}BAD ENDING - FROZEN{/size}"
    return

label ending_despair:
    scene bg shelter
    hide screen stats_overlay
    show elara sad
    e "What's the point, Keeper?"
    "Elara walks out into the snow."
    "{size=50}BAD ENDING - GIVEN UP{/size}"
    return
