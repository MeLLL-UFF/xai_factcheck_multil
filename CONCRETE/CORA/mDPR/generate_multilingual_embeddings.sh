for l in pt
do 
    python3 /content/drive/MyDrive/Concrete_Lightweight/CONCRETE/CORA/mDPR/generate_dense_embeddings.py \
    --model_file /content/drive/MyDrive/Concrete_Lightweight/CONCRETE/data/models/mDPR_biencoder_best.cpt \
    --batch_size 64 \
    --ctx_file "/content/drive/MyDrive/Concrete_Lightweight/CONCRETE/data/bbc_passages/$l/ " \
    --out_file "/content/drive/MyDrive/Concrete_Lightweight/CONCRETE/data/embeddings_multilingual/emb_$l.pkl"
done