import pymol
import pymol.preset
from tqdm import tqdm
from pymol import cmd
from pathlib import Path

def render(args, frames_path):
    proj_dir = args.proj
    complex_dir = rf'{proj_dir}\{args.complex}'
    pocket_dir = rf'{proj_dir}\{args.complex}pocket'

    cmd.cd(proj_dir)
    cmd.bg_color("white")
    pymol.setting.set("ray_opaque_background", 1)
    cmd.set("ray_shadows", "off")

    view = (\
     0.398980200,   -0.908527136,    0.123760745,\
     0.579830289,    0.145427063,   -0.801601827,\
     0.710301995,    0.391598493,    0.584833622,\
     0.000000000,    0.000000000,  -75.633140564,\
    36.915332794,   30.366722107,   40.782566071,\
    61.229915619,   90.036354065,  -20.000000000 )


    if args.antialias:
        cmd.set("antialias", "2")

    for i in tqdm(range(100), desc="Rendering"):
        complexname = rf"{complex_dir}\5H6V_MD_frame{i}.pdb"
        pocketname = rf"{pocket_dir}\5H6V_MD_frame{i}.pdb"
        object_name = rf"frame_{i}"
        pre_object_name = rf"frame_{i-1}" if i > 0 else object_name

        cmd.load(complexname, object_name)
        cmd.hide("everything")

        if i > 1:
            cmd.select("pre", f"{object_name} and resn MOL")
            cmd.select("cur", f"{pre_object_name} and resn MOL")
            cmd.align("pre", "cur")
            # cmd.delete(pre_object_name)

        # protein
        cmd.show_as("cartoon", object_name)
        cmd.util.cbaw(object_name)

        # ligand
        cmd.select("mol", f"{object_name} and resn MOL")
        cmd.show_as("licorice", "mol")
        cmd.util.cbac("mol")

        # pocket
        cmd.load(pocketname, "pocket")
        cmd.remove("elem H and pocket")
        cmd.select("pocket_mol", "pocket and resn MOL")
        cmd.remove("pocket_mol")

        cmd.show_as("surface", "pocket")
        cmd.set("transparency", "0.35", "pocket")
        cmd.set("surface_color", "wheat", "pocket")
        # cmd.color('wheat', 'pocket and surface')

        cmd.show("sticks", "pocket")
        cmd.set("stick_color", "yellow", "pocket")
        # cmd.color('yellow', 'pocket and sticks')
        # cmd.select('ca', 'pocket and (resn ALA+CYS+ASP+GLU+PHE+GLY+HIS+ILE+LYS+LEU+MET+ASN+PRO+GLN+ARG+SER+THR+VAL+TRP+TYR) \
        #            and elem C and not (name C+O+N)')

        # render
        Path.mkdir(frames_path, exist_ok=True)
        output_filename = rf"{frames_path}\frame_{i}.png"
        render_config = {
            'width': args.width,
            'height': args.width,
            'ray': args.ray,
            'dpi': args.dpi
        }
        cmd.set_view(view)
        cmd.png(output_filename, **render_config)

        cmd.delete("pocket")

    cmd.refresh()
