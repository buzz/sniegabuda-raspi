import os
from os.path import exists, join
from collections import OrderedDict

VOXELSPACES_ROOT_FOLDER = 'data/voxelspaces/'

def folder_looks_good(folder_name):
	folder_path = join(VOXELSPACES_ROOT_FOLDER, folder_name)
	settings_exist = bool([name for name in os.listdir(folder_path) if name.startswith('settings') and name.endswith('.json')])
	layers_folder = join(folder_path, 'layers')
	layers_exist = exists(layers_folder) and bool(os.listdir(layers_folder))
	return settings_exist and layers_exist



available_voxelspaces = []

for folder_name in os.listdir(VOXELSPACES_ROOT_FOLDER):
	folder_path = join(VOXELSPACES_ROOT_FOLDER, folder_name)
	settings_files = [name for name in os.listdir(folder_path) if name.startswith('settings') and name.endswith('.json')]
	if not settings_files: continue
	layers_folder = join(folder_path, 'layers')
	layers_exist = exists(layers_folder) and bool(os.listdir(layers_folder))
	if not layers_exist: continue
	available_voxelspaces.append((folder_name, settings_files))

print available_voxelspaces
