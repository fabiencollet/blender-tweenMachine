# blender-tweenMachine
 Create break down poses in Blender,
 inspired by the original tweenMachine 
 from [Justin Barrett](http://www.justinsbarrett.com/) in Maya. 

# Features
- Tween transforms and customs properties of Pose Bones (like the hotkey <kbd>Shift+E</kbd>), Objects 
  and subtypes like (Mesh, Lights, Camera, etc...)
  
- Insert Key automatically on channels who already have a fCurve.

# Usage
## Panel
![blender-tweenMachine](docs/tween_panel.gif)
## Menu
![blender-tweenMachine](docs/tween_menu.gif)
## Search operator (F3)
![blender-tweenMachine](docs/tween_search_op.gif)

# Installation

### First Method : Clone the repository
1. Open a terminal
2. Change directory to the add-ons folder in your blender user preferences folder : 
   `<BLENDER_PREFERENCES_FOLDER> > scripts > addons`
3. Clone the repository with git command.
6. Open Blender
7. Go to '''Edit > Preference > Add-ons''' and enable the "Tween Machine" add-ons

### Second Method : Download the addon and install it
1. Download the repository(.zip)
2. In Blender Go to the preference window `Edit > Preferences`
3. Click on `Addon` in the left panel
4. Click on `install...` on the top right
5. Browse and select the zip file previously download
   and click on the button `Install Add-ons` on the bottom    
6. Close and re-open Blender
7. Go to `Edit > Preference > Add-ons` and enable the "Tween Machine" add-ons

# To-Do
- [X] Tween customs properties
- [X] Insert key only on existing fCurves
- [ ] Detect customs properties of the Armature in Pose Mode context
