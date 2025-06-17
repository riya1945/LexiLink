def split_text(text,chunk_size=2000,overlap=200):
    chunks=[]
    start=0
    while start<len(text):
        end= min(start+chunk_size,len(text))
        chunks.append(text[start:end])
        start+=chunk_size-overlap
    return chunks    
