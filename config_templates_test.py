import argparse

config_elliot = """experiment:
  backend: pytorch
  data_config:
    strategy: fixed
    train_path: ../data/{{0}}/train_indexed.tsv
    validation_path: ../data/{{0}}/val_indexed.tsv
    test_path: ../data/{{0}}/test_indexed.tsv
    side_information:
      - dataloader: VisualAttribute
        visual_features: ../data/{{0}}/visual_embeddings_indexed_{batch_size}/{visual_path}
      - dataloader: TextualAttribute
        textual_features: ../data/{{0}}/textual_embeddings_indexed_{batch_size}/{textual_path}
  dataset: {dataset}
  top_k: 50
  evaluation:
    cutoffs: [ 10, 20, 50 ]
    simple_metrics: [ Recall, Precision, nDCG, HR ]
  gpu: 0
  external_models_path: ../external/models/__init__.py
  models:
    external.VBPR:
      meta:
        hyper_opt_alg: grid
        verbose: True
        save_weights: False
        save_recs: False
        validation_rate: 10
        validation_metric: Recall@20
        restore: False
      lr: [ 0.0001, 0.0005, 0.001, 0.005, 0.01 ]
      modalities: ('visual', 'textual')
      epochs: 200
      factors: 64
      batch_size: 1024
      l_w: [ 1e-5, 1e-2 ]
      comb_mod: concat
      loaders: ('VisualAttribute', 'TextualAttribute')
      seed: 123
    external.BM3:
      meta:
        hyper_opt_alg: grid
        verbose: True
        save_weights: False
        save_recs: False
        validation_rate: 10
        validation_metric: Recall@20
        restore: False
      lr: [ 0.0001, 0.0005, 0.001, 0.005, 0.01 ]
      multimod_factors: 64
      reg_weight: [ 0.1, 0.01 ]
      cl_weight: 2.0
      dropout: 0.3
      n_layers: 2
      modalities: ('visual', 'textual')
      loaders: ('VisualAttribute', 'TextualAttribute')
      epochs: 200
      factors: 64
      lr_sched: (1.0,50)
      batch_size: 1024
      seed: 123
    external.FREEDOM:
      meta:
        hyper_opt_alg: grid
        verbose: True
        save_weights: False
        save_recs: False
        validation_rate: 10
        validation_metric: Recall@20
        restore: False
      lr: [ 0.0001, 0.0005, 0.001, 0.005, 0.01 ]
      factors: 64
      epochs: 200
      l_w: [ 1e-5, 1e-2 ]
      n_layers: 1
      n_ui_layers: 2
      top_k: 10
      factors_multimod: 64
      modalities: ('visual', 'textual')
      loaders: ('VisualAttribute', 'TextualAttribute')
      mw: (0.1,0.9)
      drop: 0.8
      lr_sched: (1.0,50)
      batch_size: 1024
      seed: 123
      
"""


config_ducho = """dataset_path: ./local/data/demo_{dataset}
gpu list: 0

visual_textual:
    items:
        input_path: {{visual: images, textual: meta.tsv}}
        item_column: asin
        text_column: description
        output_path: {{visual: visual_embeddings_{batch_size}, textual: textual_embeddings_{batch_size}}}
        model: [
            {{ model_name: kakaobrain/align-base, backend: transformers, output_layers: 1, batch_size: {batch_size}}},
            {{ model_name: BAAI/AltCLIP, backend: transformers, output_layers: 1, batch_size: {batch_size}}},
        ]
        
"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Training script for ResNet with BPR.")
    parser.add_argument('--dataset', choices=['baby', 'office', 'music'], help="Dataset name.", required=True)
    parser.add_argument('--batch_size', type=int, help="Batch size.", required=True)


    args = parser.parse_args()

    demo_4 = {
        "visual_path": "transformers/kakaobrain/align-base/1",
        "textual_path": "transformers/kakaobrain/align-base/1"
    }

    elliot_4 = config_elliot.format(
        batch_size=args.batch_size,
        dataset=args.dataset,
        visual_path=demo_4["visual_path"],
        textual_path=demo_4["textual_path"]
        )
    
    elliot_dir = f"/home/matteo/Formal-Multimod-Rec/config_files/{args.dataset}_4_{args.batch_size}.yml"

    with open(elliot_dir, 'w') as conf_file:
        conf_file.write(elliot_4)

    del elliot_4, demo_4, elliot_dir
    
    demo_5 = {
        "visual_path": "transformers/BAAI/AltCLIP/1",
        "textual_path": "transformers/BAAI/AltCLIP/1"
    }

    elliot_5 = config_elliot.format(
        batch_size=args.batch_size,
        dataset=args.dataset,
        visual_path=demo_5["visual_path"],
        textual_path=demo_5["textual_path"]
        )
    
    elliot_dir = f"/home/matteo/Formal-Multimod-Rec/config_files/{args.dataset}_5_{args.batch_size}.yml"

    with open(elliot_dir, 'w') as conf_file:
        conf_file.write(elliot_5)

    del elliot_5, demo_5, elliot_dir

    ducho = config_ducho.format(
        dataset=args.dataset,
        batch_size=args.batch_size
    )

    ducho_dir = f"/home/matteo/Ducho/demos/demo_{args.dataset}/config.yml"
    with open(ducho_dir, 'w') as conf_file:
        conf_file.write(ducho)
