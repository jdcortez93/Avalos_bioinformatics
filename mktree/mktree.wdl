version 1.0

workflow mktreeWorkflow {
    input {
        String prefix
        File infile
    }

    parameter_meta {
        infile: "Unaligned homologous protein sequences in FASTA format. Sequence names must be unique."
        prefix: "The name of the protein, used to name output."
    }

    call validateTask {
        input: 
            infile = infile
    }

    call clustaloTask {
        input: 
            prefix = prefix, 
            infile = infile
    }

    call trimalTask {
        input: 
            prefix = prefix, 
            infile = clustaloTask.outfile
    }

    call fasttreeTask {
        input: 
            prefix = prefix, 
            infile = trimalTask.outfile
    }

    call hmmbuildTask {
        input: 
            prefix = prefix, 
            infile = clustaloTask.outfile
    }

    output {
        File msa = clustaloTask.outfile
        File tree = fasttreeTask.outfile
        File hmm = hmmbuildTask.outfile
    }
}

# verify sequence identifiers are unique
task validateTask {
    input {
        File infile
    }
    
    parameter_meta {
        infile: "Unaligned homologous protein sequences in FASTA format"
    }

    command <<<
        (( `grep '^>' | cut -f 1 -d ' ' | sort | uniq -d | wc -l | xargs` == 0 ))
    >>>
}

task clustaloTask {
    input {
        File infile
        String prefix
    }

    parameter_meta {
        infile: "Unaligned homologous protein sequences in FASTA format"
        prefix: "The name of the protein, used to name output"
    }

    command <<<
        clustalo --threads 8 \
            -i ~{infile} \
            --dealign -t Protein \
            --infmt=fasta \
            --outfmt=fasta \
            -o ~{prefix}.msa.fasta
    >>>

    runtime {
        docker: "evolbioinfo/clustal_omega:v1.2.4"
        memory: "30G"
        cpu: 8
    }

    output {
        File outfile = "${prefix}.msa.fasta"
    }
}

task trimalTask {
    input {
        File infile
        String prefix
    }

    parameter_meta {
        infile: "Aligned homologous protein sequences in FASTA format"
        prefix: "The name of the protein, used to name output"
    }

    command <<<
        trimal -gt 0.2 \
            -cons 0.8 \
            -resoverlap 0.2 \
            -seqoverlap 0.0 \
            -in ~{infile} \
            -out ~{prefix}.trimal.fasta
    >>>

    runtime {
        docker: "evolbioinfo/trimal:v1.4.1"
        memory: "30G"
        cpu: 8
    }

    output {
        File outfile = "${prefix}.trimal.fasta"
    }
}

task fasttreeTask {
    input {
        File infile
        String prefix
    }

    parameter_meta {
        infile: "Aligned homologous protein sequences with noninformative columns removed, in FASTA format"
        prefix: "The name of the protein, used to name output"
    }

    command <<<
        FastTree -wag -gamma ~{infile} > ~{prefix}.tre
    >>>

    runtime {
        docker: "evolbioinfo/fasttree:v2.1.11"
        memory: "30G"
        cpu: 1
    }

    output {
        File outfile = "${prefix}.tre"
    }
}

task hmmbuildTask {
    input {
        File infile
        String prefix
    }

    parameter_meta {
        infile: "Aligned homologous protein sequences in FASTA format"
        prefix: "The name of the protein, used to name output"
    }

    command <<<
        hmmbuild -n ~{prefix} ~{prefix}.hmm ~{infile}
    >>>

    runtime {
        docker: "evolbioinfo/hmmer:v3.3"
        memory: "30G"
        cpu: 1
    }

    output {
        File outfile = "${prefix}.hmm"
    }
}
