import argparse

config = """dataset_path: ./local/data/demo_{dataset}
gpu list: 0

visual:
    items:
        input_path: images
        output_path: visual_embeddings_{batch_size}
        model: [
                {{ model_name: ResNet50,  output_layers: avgpool, reshape: [224, 224], preprocessing: zscore, backend: torch, batch_size: {batch_size}}},
                {{ model_name: ./demos/demo_{dataset}/MMFashion.pt,  output_layers: avgpool, reshape: [224, 224], preprocessing: zscore, backend: torch, batch_size: {batch_size}}},
        ]

textual:
    items:
        input_path: meta.tsv
        item_column: asin
        text_column: description
        output_path: textual_embeddings_{batch_size}
        model: [
            {{ model_name: sentence-transformers/all-mpnet-base-v2,  output_layers: 1, clear_text: False, backend: sentence_transformers, batch_size: {batch_size}}},
          ]

visual_textual:
    items:
        input_path: {{visual: images, textual: meta.tsv}}
        item_column: asin
        text_column: description
        output_path: {{visual: visual_embeddings_{batch_size}, textual: textual_embeddings_{batch_size}}}
        model: [
            {{ model_name: openai/clip-vit-base-patch16, backend: transformers, output_layers: 1, batch_size: {batch_size}}},
            {{ model_name: kakaobrain/align-base, backend: transformers, output_layers: 1, batch_size: {batch_size}}},
            {{ model_name: BAAI/AltCLIP, backend: transformers, output_layers: 1, batch_size: {batch_size}}},
        ]
        
"""



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', choices=['baby', 'office', 'music', 'toys', 'beauty'], help="Dataset name.", required=True)
    parser.add_argument('--batch_size', type=int, help="Batch size.", required=True)


    args = parser.parse_args()

    ducho = config.format(
        dataset=args.dataset,
        batch_size=args.batch_size
    )

    ducho_dir = f"./Ducho/demos/demo_{args.dataset}/config.yml"
    with open(ducho_dir, 'w') as conf_file:
        conf_file.write(ducho)
