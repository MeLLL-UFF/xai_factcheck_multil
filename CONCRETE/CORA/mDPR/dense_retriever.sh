mkdir retrieved_docs/
for f in train.all dev.all test.all ood zeroshot;
do
    # X-ICT
    python3 /content/drive/MyDrive/Concrete_Lightweight/CONCRETE/CORA/mDPR/dense_retriever.py \
    --model_file "/content/drive/MyDrive/Concrete_Lightweight/CONCRETE/checkpoints/xICT_biencoder.pt.37.9188" \
    --ctx_file "/content/drive/MyDrive/Concrete_Lightweight/CONCRETE/data/bbc_passages" \
    --claim_file /content/drive/MyDrive/Concrete_Lightweight/CONCRETE/data/x-fact/$f.tsv \
    --encoded_dir ./embeddings_multilingual/ 
    --out_file retrieved_docs/$f.xict.json --batch_size 64 --n-docs 100
    
done
