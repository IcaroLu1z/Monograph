from sklearn.manifold import TSNE
import umap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

authors_data = pd.read_csv('/media/work/icarovasconcelos/mono/data/authors-information.csv')

# Parameters
visual_random_state = 0
kmeans_random_state = 0

# List of embeddings files
embeddings_files = [
 
   
]

kmeans_files = [

]


ward_files = [
  
]


# Initialize lists to store the figures and titles
titles = []
tsne_paths = []
umap_paths = []

model_name, models_path = 'kmeans', kmeans_files
#model_name, models_path = 'Ward', ward_files

# Iterate over the list of files
for embeddings_path, model_path in zip(embeddings_files, models_path):
    # Load your embeddings
    embeddings_dict = np.load(embeddings_path, allow_pickle=True).item()
    
    # Convert dictionary values to a list of embeddings
    embeddings = np.array(list(embeddings_dict.values()))

    # Load the K-Means model
    model = pickle.load(open(model_path, "rb"))
    model_labels = model.labels_

    # Get gp_score labels
    gp_scores = [authors_data.loc[authors_data['author_id'] == key, 'gp_score'].values[0] 
                 for key in embeddings_dict.keys()]
    
    # Extract parameters from the file name for the subtitle
    params = embeddings_path.split('_')[-6:]  # Adjust this based on your file name structure
    subtitle = f'{params[-5]}_{params[-4]}_{params[-3]}_{params[-2]}_{params[-1]}'
    titles.append(subtitle)
    
    # Initialize the plots
    fig_tsne, axs_tsne = plt.subplots(1, 2, figsize=(12, 6))
    
    # Perform t-SNE
    tsne = TSNE(n_components=2, random_state=visual_random_state)
    tsne_result = tsne.fit_transform(embeddings)

    # Plot t-SNE with K-Means labels
    scatter1 = axs_tsne[0].scatter(tsne_result[:, 0], tsne_result[:, 1], c=model_labels, cmap='viridis')
    legend1 = axs_tsne[0].legend(*scatter1.legend_elements(), title=f"{model_name} Clusters")
    axs_tsne[0].add_artist(legend1)
    axs_tsne[0].set_title(f't-SNE with {model_name} Clustering\n{subtitle}')

    # Plot t-SNE with gp_score labels
    scatter2 = axs_tsne[1].scatter(tsne_result[:, 0], tsne_result[:, 1], c=gp_scores, cmap='plasma')
    legend2 = axs_tsne[1].legend(*scatter2.legend_elements(), title="gp_scores")
    axs_tsne[1].add_artist(legend2)
    axs_tsne[1].set_title(f't-SNE with gp_scores\n{subtitle}')
    
    # Save the figure
    tsne_paths.append(f'/media/work/icarovasconcelos/mono/results/figures/{model_name}_tsne_{subtitle}.png')
    plt.savefig(tsne_paths[-1])
    plt.close()
    
    # Initialize the UMAP plots
    fig_umap, axs_umap = plt.subplots(1, 2, figsize=(12, 6))

    # Perform UMAP
    umap_model = umap.UMAP(n_components=2, random_state=visual_random_state)
    umap_result = umap_model.fit_transform(embeddings)

    # Plot UMAP with K-Means labels
    scatter3 = axs_umap[0].scatter(umap_result[:, 0], umap_result[:, 1], c=model_labels, cmap='viridis')
    legend3 = axs_umap[0].legend(*scatter3.legend_elements(), title=f"{model_name} Clusters")
    axs_umap[0].add_artist(legend3)
    axs_umap[0].set_title(f'UMAP with {model_name} Clustering\n{subtitle}')

    # Plot UMAP with gp_score labels
    scatter4 = axs_umap[1].scatter(umap_result[:, 0], umap_result[:, 1], c=gp_scores, cmap='plasma')
    legend4 = axs_umap[1].legend(*scatter4.legend_elements(), title="gp_scores")
    axs_umap[1].add_artist(legend4)
    axs_umap[1].set_title(f'UMAP with gp_scores\n{subtitle}')
    
    # Save the figure
    umap_paths.append(f'/media/work/icarovasconcelos/mono/results/figures/{model_name}_umap_{subtitle}.png')
    plt.savefig(umap_paths[-1])
    plt.close()

def plot_images(images_paths, save_path, title):
    images = [plt.imread(image_path) for image_path in images_paths]
    
    fig, axs = plt.subplots(2, 2, figsize=(24, 12))  # Adjust figsize to control the plot size
    
    for i, ax in enumerate(axs.flatten()):
        ax.imshow(images[i])
        ax.axis('off')  # Turn off axes
        ax.set_aspect('auto')  # Ensure no scaling of images
    
    fig.suptitle(title, fontsize=16)  # Set the overall title
    plt.tight_layout()  # Adjust layout to fit title
    plt.savefig(save_path)  # Save the plot as a PNG file
    plt.close()  # Close the plot to free memory

saved_tsne_board = f'/media/work/icarovasconcelos/mono/results/figures/{model_name}_tsne_board.png'
saved_umap_board = f'/media/work/icarovasconcelos/mono/results/figures/{model_name}_umap_board.png'

# Plot and save the t-SNE images
plot_images(tsne_paths, saved_tsne_board, f'{model_name} w/ t-SNE')

# Plot and save the UMAP images
plot_images(umap_paths, saved_umap_board, f'{model_name} w/ UMAP')