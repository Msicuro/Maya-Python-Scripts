####Import/Export Skin Skin####
import pymel.core as pm
import os

def establish_data_dir():
    '''
    Create a data directory if it doesn't exist, save the file path
    if it does
    Returns: data_dir

    '''
    # Save the parent directory
    working_dir = pm.workspace(query=True, active=True)
    # Save the name for the data directory
    data_dir = os.path.join(working_dir, 'data')

    # If the data path doesn't exist, create it
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    return data_dir

def import_weights():
    '''
    Import skin weights
    Returns:

    '''
    data_dir = establish_data_dir()
    # List all files in the data  directory
    data_files = os.listdir(data_dir)

    # Save the meshes to import weights for
    if not pm.selected():
        mesh_transforms = [i for i in pm.ls(type=pm.nt.Transform) if i.getShape()]
    else:
        mesh_transforms = pm.selected(type=pm.nt.Transform)

    # Cycle through the list of meshes and find the most recent iteration
    for i in mesh_transforms:
        valid_files = [i for i in data_files if i.split("_")[0] == i.name()]

