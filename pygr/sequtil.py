
DNA_SEQTYPE=0
RNA_SEQTYPE=1
PROTEIN_SEQTYPE=2

def guess_seqtype(s):
    dna_letters='AaTtUuGgCcNn'
    ndna=0
    nU=0
    nT=0
    for l in s:
        if l in dna_letters:
            ndna += 1
        if l=='U' or l=='u':
            nU += 1
        elif l=='T' or l=='t':
            nT += 1
    ratio=ndna/float(len(s))
    if ratio>0.85:
        if nT>nU:
            return DNA_SEQTYPE
        else:
            return RNA_SEQTYPE
    else:
        return PROTEIN_SEQTYPE

seq_id_counter=0
def new_seq_id():
    global seq_id_counter
    seq_id_counter += 1
    return str(seq_id_counter-1)


def write_fasta(ofile,s,chunk=60,id=None,reformatter=None):
    "Trivial FASTA output"
    if id is None:
        try:
            id = str(s.id)
        except AttributeError:
            id = new_seq_id()

    ofile.write('>' + id + '\n')
    seq = str(s)
    if reformatter is not None: # APPLY THE DESIRED REFORMATTING
        seq = reformatter(seq)
    end = len(seq)
    pos = 0
    while 1:
        ofile.write(seq[pos:pos+chunk] + '\n')
        pos += chunk
        if pos >= end:
            break
    return id # IN CASE CALLER WANTS TEMP ID WE MAY HAVE ASSIGNED

def read_fasta(ifile):
    "iterate over id,title,seq from stream ifile"
    id = None
    isEmpty = True
    for line in ifile:
        if '>' == line[0]:
            if id is not None and len(seq) > 0:
                yield id,title,seq
                isEmpty = False
            id = line[1:].split()[0]
            title = line[len(id)+2:]
            seq = ''
        elif id is not None: # READ SEQUENCE
            for word in line.split(): # GET RID OF WHITESPACE
                seq += word
    if id is not None and len(seq) > 0:
        yield id,title,seq
    elif isEmpty:
        raise IOError('no readable sequence in FASTA file!')

def read_fasta_one_line(ifile):
    "read a single sequence line, return id,title,seq"
    id = None
    seq = ''
    while True:
        line = ifile.readline(1024) # READ AT MOST 1KB
        if line == '': # EOF
            break
        elif '>' == line[0]:
            id = line[1:].split()[0]
            title = line[len(id)+2:]
        elif id is not None: # READ SEQUENCE
            for word in line.split(): # GET RID OF WHITESPACE
                seq += word
            if len(seq)>0:
                return id,title,seq
    raise IOError('no readable sequence in FASTA file!')

def read_fasta_lengths(ifile):
    "Generate sequence ID,length from stream ifile"
    id = None
    seqLength = 0
    isEmpty = True
    for line in ifile:
        if '>' == line[0]:
            if id is not None and seqLength > 0:
                yield id,seqLength
                isEmpty = False
            id = line[1:].split()[0]
            seqLength = 0
        elif id is not None: # READ SEQUENCE
            for word in line.split(): # GET RID OF WHITESPACE
                seqLength += len(word)
    if id is not None and seqLength > 0:
        yield id,seqLength
    elif isEmpty:
        raise IOError('no readable sequence in FASTA file!')

