"""
Bioinformatics Module

This module provides comprehensive bioinformatics utilities including:
- DNA/RNA sequence analysis
- Protein sequence analysis
- Sequence alignment
- Phylogenetic tree concepts
- Gene prediction
- Motif finding
- Sequence statistics
- Translation and transcription
- Restriction enzyme sites
- Sequence visualization

All functions include comprehensive docstrings and type hints.
"""

import random
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from collections import Counter


class SequenceType(Enum):
    """Types of biological sequences."""
    DNA = "dna"
    RNA = "rna"
    PROTEIN = "protein"


class MutationType(Enum):
    """Types of mutations."""
    SUBSTITUTION = "substitution"
    INSERTION = "insertion"
    DELETION = "deletion"
    INVERSION = "inversion"


@dataclass
class Sequence:
    """Biological sequence data structure."""
    sequence: str
    sequence_type: SequenceType
    id: str = ""
    description: str = ""
    quality: Optional[str] = None
    
    def __len__(self) -> int:
        """Get sequence length."""
        return len(self.sequence)
    
    def reverse_complement(self) -> 'Sequence':
        """Get reverse complement (for DNA)."""
        if self.sequence_type != SequenceType.DNA:
            return self
        
        complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',
                     'a': 't', 't': 'a', 'g': 'c', 'c': 'g',
                     'N': 'N', 'n': 'n'}
        
        rev_comp = ""
        for base in reversed(self.sequence):
            rev_comp += complement.get(base, base)
        
        return Sequence(
            sequence=rev_comp,
            sequence_type=self.sequence_type,
            id=self.id + "_rc",
            description=self.description
        )


class SequenceUtils:
    """General sequence utilities."""
    
    @staticmethod
    def validate_sequence(sequence: str, seq_type: SequenceType) -> bool:
        """Validate sequence characters."""
        valid_chars = {
            SequenceType.DNA: set('ATGCNatgcn'),
            SequenceType.RNA: set('AUGCNaugcn'),
            SequenceType.PROTEIN: set('ACDEFGHIKLMNPQRSTVWY*acdefghiklmnpqrstvwy*')
        }
        
        valid = valid_chars.get(seq_type, set())
        return all(char in valid for char in sequence)
    
    @staticmethod
    def calculate_gc_content(sequence: str) -> float:
        """Calculate GC content of DNA sequence."""
        sequence = sequence.upper()
        gc_count = sequence.count('G') + sequence.count('C')
        total = len(sequence)
        
        return (gc_count / total * 100) if total > 0 else 0.0
    
    @staticmethod
    def calculate_at_content(sequence: str) -> float:
        """Calculate AT content of DNA sequence."""
        sequence = sequence.upper()
        at_count = sequence.count('A') + sequence.count('T')
        total = len(sequence)
        
        return (at_count / total * 100) if total > 0 else 0.0
    
    @staticmethod
    def translate_dna_to_rna(dna_sequence: str) -> str:
        """Transcribe DNA to RNA."""
        return dna_sequence.replace('T', 'U').replace('t', 'u')
    
    @staticmethod
    def translate_rna_to_dna(rna_sequence: str) -> str:
        """Translate RNA to DNA."""
        return rna_sequence.replace('U', 'T').replace('u', 't')
    
    @staticmethod
    def reverse_sequence(sequence: str) -> str:
        """Reverse sequence."""
        return sequence[::-1]


class CodonTable:
    """Genetic code table for translation."""
    
    STANDARD_GENETIC_CODE = {
        'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
        'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
        'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
        'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
        'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
        'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
        'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
        'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }
    
    @staticmethod
    def translate_rna_to_protein(rna_sequence: str) -> str:
        """Translate RNA sequence to protein."""
        protein = ""
        
        for i in range(0, len(rna_sequence) - 2, 3):
            codon = rna_sequence[i:i+3].upper()
            amino_acid = CodonTable.STANDARD_GENETIC_CODE.get(codon, 'X')
            protein += amino_acid
        
        return protein
    
    @staticmethod
    def translate_dna_to_protein(dna_sequence: str) -> str:
        """Translate DNA sequence to protein."""
        rna = SequenceUtils.translate_dna_to_rna(dna_sequence)
        return CodonTable.translate_rna_to_protein(rna)


class SequenceAlignment:
    """Sequence alignment algorithms."""
    
    @staticmethod
    def needleman_wunsch(seq1: str, seq2: str, 
                        match_score: int = 1, 
                        mismatch_penalty: int = -1,
                        gap_penalty: int = -1) -> Tuple[str, str, int]:
        """Needleman-Wunsch global alignment."""
        m, n = len(seq1), len(seq2)
        
        # Initialize scoring matrix
        score = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Initialize first row and column
        for i in range(m + 1):
            score[i][0] = i * gap_penalty
        for j in range(n + 1):
            score[0][j] = j * gap_penalty
        
        # Fill scoring matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                match = score[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty)
                delete = score[i-1][j] + gap_penalty
                insert = score[i][j-1] + gap_penalty
                
                score[i][j] = max(match, delete, insert)
        
        # Traceback
        aligned1, aligned2 = "", ""
        i, j = m, n
        
        while i > 0 or j > 0:
            if i > 0 and j > 0:
                current = score[i][j]
                diagonal = score[i-1][j-1]
                
                if seq1[i-1] == seq2[j-1]:
                    expected = diagonal + match_score
                else:
                    expected = diagonal + mismatch_penalty
                
                if current == expected:
                    aligned1 = seq1[i-1] + aligned1
                    aligned2 = seq2[j-1] + aligned2
                    i -= 1
                    j -= 1
                    continue
            
            if i > 0 and score[i][j] == score[i-1][j] + gap_penalty:
                aligned1 = seq1[i-1] + aligned1
                aligned2 = "-" + aligned2
                i -= 1
            elif j > 0:
                aligned1 = "-" + aligned1
                aligned2 = seq2[j-1] + aligned2
                j -= 1
        
        return aligned1, aligned2, score[m][n]
    
    @staticmethod
    def smith_waterman(seq1: str, seq2: str,
                      match_score: int = 2,
                      mismatch_penalty: int = -1,
                      gap_penalty: int = -1) -> Tuple[str, str, int]:
        """Smith-Waterman local alignment."""
        m, n = len(seq1), len(seq2)
        
        # Initialize scoring matrix
        score = [[0] * (n + 1) for _ in range(m + 1)]
        max_score = 0
        max_pos = (0, 0)
        
        # Fill scoring matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                match = score[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty)
                delete = score[i-1][j] + gap_penalty
                insert = score[i][j-1] + gap_penalty
                
                score[i][j] = max(0, match, delete, insert)
                
                if score[i][j] > max_score:
                    max_score = score[i][j]
                    max_pos = (i, j)
        
        # Traceback from max position
        aligned1, aligned2 = "", ""
        i, j = max_pos
        
        while i > 0 and j > 0 and score[i][j] > 0:
            if i > 0 and j > 0:
                current = score[i][j]
                diagonal = score[i-1][j-1]
                
                if seq1[i-1] == seq2[j-1]:
                    expected = diagonal + match_score
                else:
                    expected = diagonal + mismatch_penalty
                
                if current == expected:
                    aligned1 = seq1[i-1] + aligned1
                    aligned2 = seq2[j-1] + aligned2
                    i -= 1
                    j -= 1
                    continue
            
            if i > 0 and score[i][j] == score[i-1][j] + gap_penalty:
                aligned1 = seq1[i-1] + aligned1
                aligned2 = "-" + aligned2
                i -= 1
            elif j > 0:
                aligned1 = "-" + aligned1
                aligned2 = seq2[j-1] + aligned2
                j -= 1
        
        return aligned1, aligned2, max_score


class SequenceStatistics:
    """Sequence statistics and analysis."""
    
    @staticmethod
    def calculate_composition(sequence: str) -> Dict[str, int]:
        """Calculate nucleotide/amino acid composition."""
        sequence = sequence.upper()
        composition = Counter(sequence)
        return dict(composition)
    
    @staticmethod
    def find_orfs(sequence: str, min_length: int = 100) -> List[Tuple[int, int, str]]:
        """Find open reading frames (simplified)."""
        orfs = []
        start_codon = 'ATG'
        stop_codons = {'TAA', 'TAG', 'TGA'}
        
        for frame in range(3):
            i = frame
            start_pos = -1
            
            while i < len(sequence) - 2:
                codon = sequence[i:i+3].upper()
                
                if codon == start_codon and start_pos == -1:
                    start_pos = i
                elif codon in stop_codons and start_pos != -1:
                    orf_length = i - start_pos + 3
                    if orf_length >= min_length:
                        orf_sequence = sequence[start_pos:i+3]
                        orfs.append((start_pos, i+3, orf_sequence))
                    start_pos = -1
                
                i += 3
        
        return orfs
    
    @staticmethod
    def calculate_molecular_weight(dna_sequence: str) -> float:
        """Calculate molecular weight of DNA sequence."""
        weights = {'A': 331.0, 'T': 322.0, 'G': 347.0, 'C': 307.0}
        
        sequence = dna_sequence.upper()
        total_weight = 0.0
        
        for base in sequence:
            total_weight += weights.get(base, 0)
        
        return total_weight
    
    @staticmethod
    def calculate_melting_temperature(dna_sequence: str) -> float:
        """Calculate melting temperature (simplified)."""
        sequence = dna_sequence.upper()
        length = len(sequence)
        
        if length < 14:
            # Short sequences
            at_count = sequence.count('A') + sequence.count('T')
            gc_count = sequence.count('G') + sequence.count('C')
            tm = 2 * at_count + 4 * gc_count
        else:
            # Long sequences
            gc_content = SequenceUtils.calculate_gc_content(sequence)
            tm = 64.9 + 41 * (gc_content - 16.4) / 100
        
        return tm


class MotifFinder:
    """Motif finding algorithms."""
    
    @staticmethod
    def find_motif(sequence: str, motif: str) -> List[int]:
        """Find all occurrences of motif in sequence."""
        positions = []
        motif_lower = motif.lower()
        sequence_lower = sequence.lower()
        
        i = 0
        while i < len(sequence) - len(motif) + 1:
            if sequence_lower[i:i+len(motif)] == motif_lower:
                positions.append(i)
                i += len(motif)
            else:
                i += 1
        
        return positions
    
    @staticmethod
    def find_consensus_motif(sequences: List[str], motif_length: int = 6) -> str:
        """Find consensus motif from multiple sequences."""
        if not sequences:
            return ""
        
        # Extract all possible motifs
        all_motifs = []
        
        for seq in sequences:
            for i in range(len(seq) - motif_length + 1):
                motif = seq[i:i+motif_length].upper()
                all_motifs.append(motif)
        
        if not all_motifs:
            return ""
        
        # Find most common motif
        motif_counts = Counter(all_motifs)
        consensus = motif_counts.most_common(1)[0][0]
        
        return consensus
    
    @staticmethod
    def find_palindromes(sequence: str, min_length: int = 4) -> List[Tuple[int, int, str]]:
        """Find palindromic sequences."""
        palindromes = []
        sequence = sequence.upper()
        
        for i in range(len(sequence)):
            for j in range(i + min_length, len(sequence) + 1):
                substring = sequence[i:j]
                if substring == substring[::-1]:
                    palindromes.append((i, j, substring))
        
        return palindromes


class RestrictionEnzyme:
    """Restriction enzyme utilities."""
    
    @staticmethod
    def find_restriction_sites(sequence: str, recognition_site: str) -> List[int]:
        """Find restriction enzyme recognition sites."""
        positions = []
        site_upper = recognition_site.upper()
        sequence_upper = sequence.upper()
        
        i = 0
        while i < len(sequence) - len(recognition_site) + 1:
            if sequence_upper[i:i+len(recognition_site)] == site_upper:
                positions.append(i)
                i += len(recognition_site)
            else:
                i += 1
        
        return positions
    
    @staticmethod
    def digest_sequence(sequence: str, recognition_sites: List[str]) -> List[str]:
        """Digest sequence with multiple restriction enzymes."""
        cut_positions = set()
        
        for site in recognition_sites:
            positions = RestrictionEnzyme.find_restriction_sites(sequence, site)
            cut_positions.update(positions)
        
        cut_positions = sorted(cut_positions)
        
        fragments = []
        prev_pos = 0
        
        for pos in cut_positions:
            fragments.append(sequence[prev_pos:pos])
            prev_pos = pos
        
        fragments.append(sequence[prev_pos:])
        
        return fragments


class PhylogeneticTree:
    """Simple phylogenetic tree concepts."""
    
    @staticmethod
    def calculate_distance_matrix(sequences: List[str]) -> List[List[float]]:
        """Calculate pairwise distance matrix."""
        n = len(sequences)
        distance_matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                # Calculate Hamming distance
                seq1 = sequences[i]
                seq2 = sequences[j]
                
                # Align sequences (simplified - assume same length)
                min_len = min(len(seq1), len(seq2))
                mismatches = sum(1 for k in range(min_len) if seq1[k] != seq2[k])
                
                distance = mismatches / min_len if min_len > 0 else 0
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance
        
        return distance_matrix
    
    @staticmethod
    def upgma_clustering(distance_matrix: List[List[float]]) -> Dict:
        """UPGMA clustering (simplified)."""
        n = len(distance_matrix)
        clusters = [{i} for i in range(n)]
        
        while len(clusters) > 1:
            # Find closest clusters
            min_dist = float('inf')
            merge_i, merge_j = -1, -1
            
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    # Calculate cluster distance (average)
                    dist = 0
                    count = 0
                    
                    for ci in clusters[i]:
                        for cj in clusters[j]:
                            dist += distance_matrix[ci][cj]
                            count += 1
                    
                    avg_dist = dist / count if count > 0 else 0
                    
                    if avg_dist < min_dist:
                        min_dist = avg_dist
                        merge_i, merge_j = i, j
            
            # Merge clusters
            if merge_i != -1 and merge_j != -1:
                clusters[merge_i] = clusters[merge_i].union(clusters[merge_j])
                clusters.pop(merge_j)
        
        return {"clusters": clusters}


class SequenceVisualization:
    """Sequence visualization utilities."""
    
    @staticmethod
    def format_sequence_with_line_numbers(sequence: str, line_length: int = 60) -> str:
        """Format sequence with line numbers."""
        formatted = []
        
        for i in range(0, len(sequence), line_length):
            line_num = i // line_length + 1
            line = sequence[i:i+line_length]
            formatted.append(f"{line_num:5d}: {line}")
        
        return "\n".join(formatted)
    
    @staticmethod
    def create_dot_plot(seq1: str, seq2: str, window_size: int = 1) -> str:
        """Create simple dot plot visualization."""
        plot = []
        
        for i, base1 in enumerate(seq1):
            row = []
            for j, base2 in enumerate(seq2):
                if base1 == base2:
                    row.append("*")
                else:
                    row.append(" ")
            plot.append("".join(row))
        
        return "\n".join(plot)


class GenePrediction:
    """Simple gene prediction utilities."""
    
    @staticmethod
    def predict_coding_regions(sequence: str, min_orf_length: int = 300) -> List[Dict]:
        """Predict coding regions based on ORFs."""
        orfs = SequenceStatistics.find_orfs(sequence, min_orf_length)
        
        predictions = []
        for start, end, orf_seq in orfs:
            protein = CodonTable.translate_dna_to_protein(orf_seq)
            
            predictions.append({
                "start": start,
                "end": end,
                "length": end - start,
                "protein": protein,
                "or_sequence": orf_seq
            })
        
        return predictions


def demonstrate_bioinformatics():
    """Demonstrate bioinformatics functionality."""
    print("=== Bioinformatics Demonstration ===\n")
    
    # Sequence Validation
    print("1. Sequence Validation:")
    dna_seq = "ATCGATCGATCG"
    rna_seq = "AUCGAUCGAUCG"
    protein_seq = "ACDEFGHIKLM"
    
    print(f"   DNA valid: {SequenceUtils.validate_sequence(dna_seq, SequenceType.DNA)}")
    print(f"   RNA valid: {SequenceUtils.validate_sequence(rna_seq, SequenceType.RNA)}")
    print(f"   Protein valid: {SequenceUtils.validate_sequence(protein_seq, SequenceType.PROTEIN)}")
    
    # GC Content
    print("\n2. GC Content:")
    gc_content = SequenceUtils.calculate_gc_content(dna_seq)
    at_content = SequenceUtils.calculate_at_content(dna_seq)
    print(f"   GC content: {gc_content:.2f}%")
    print(f"   AT content: {at_content:.2f}%")
    
    # Transcription and Translation
    print("\n3. Transcription and Translation:")
    rna = SequenceUtils.translate_dna_to_rna(dna_seq)
    print(f"   DNA: {dna_seq}")
    print(f"   RNA: {rna}")
    
    protein = CodonTable.translate_dna_to_protein(dna_seq)
    print(f"   Protein: {protein}")
    
    # Reverse Complement
    print("\n4. Reverse Complement:")
    dna = Sequence(dna_seq, SequenceType.DNA)
    rev_comp = dna.reverse_complement()
    print(f"   Original: {dna.sequence}")
    print(f"   Reverse complement: {rev_comp.sequence}")
    
    # Sequence Alignment
    print("\n5. Sequence Alignment:")
    seq1 = "GATTACA"
    seq2 = "GCATGCU"
    
    aligned1, aligned2, score = SequenceAlignment.needleman_wunsch(seq1, seq2)
    print(f"   Global alignment:")
    print(f"   {aligned1}")
    print(f"   {aligned2}")
    print(f"   Score: {score}")
    
    local1, local2, local_score = SequenceAlignment.smith_waterman(seq1, seq2)
    print(f"   Local alignment:")
    print(f"   {local1}")
    print(f"   {local2}")
    print(f"   Score: {local_score}")
    
    # Sequence Statistics
    print("\n6. Sequence Statistics:")
    composition = SequenceStatistics.calculate_composition(dna_seq)
    print(f"   Composition: {composition}")
    
    orfs = SequenceStatistics.find_orfs(dna_seq + "ATGAAATAG", min_length=6)
    print(f"   ORFs found: {len(orfs)}")
    
    molecular_weight = SequenceStatistics.calculate_molecular_weight(dna_seq)
    print(f"   Molecular weight: {molecular_weight:.2f} Da")
    
    melting_temp = SequenceStatistics.calculate_melting_temperature(dna_seq)
    print(f"   Melting temperature: {melting_temp:.2f}°C")
    
    # Motif Finding
    print("\n7. Motif Finding:")
    motif = "ATG"
    positions = MotifFinder.find_motif(dna_seq, motif)
    print(f"   Motif '{motif}' positions: {positions}")
    
    consensus = MotifFinder.find_consensus_motif([dna_seq, "ATGCAT", "ATGATG"], 3)
    print(f"   Consensus motif: {consensus}")
    
    palindromes = MotifFinder.find_palindromes("GATATAG", min_length=4)
    print(f"   Palindromes: {len(palindromes)}")
    
    # Restriction Enzymes
    print("\n8. Restriction Enzymes:")
    sites = RestrictionEnzyme.find_restriction_sites(dna_seq, "ATCG")
    print(f"   Restriction sites: {sites}")
    
    fragments = RestrictionEnzyme.digest_sequence(dna_seq + "ATCG" + dna_seq, ["ATCG"])
    print(f"   Fragments: {len(fragments)}")
    
    # Phylogenetic Tree
    print("\n9. Phylogenetic Tree:")
    sequences = ["ATCG", "ATCC", "GTCG", "GTCC"]
    distance_matrix = PhylogeneticTree.calculate_distance_matrix(sequences)
    print(f"   Distance matrix: {distance_matrix}")
    
    # Sequence Visualization
    print("\n10. Sequence Visualization:")
    formatted = SequenceVisualization.format_sequence_with_line_numbers(dna_seq, line_length=10)
    print(f"   Formatted:\n{formatted}")
    
    # Gene Prediction
    print("\n11. Gene Prediction:")
    test_dna = "ATGAAATAGATGCCCCATAG"
    predictions = GenePrediction.predict_coding_regions(test_dna, min_orf_length=6)
    print(f"   Predicted genes: {len(predictions)}")
    
    print("\n=== Demonstration Complete ===")
    print("\nBioinformatics Best Practices:")
    print("- Validate sequences before processing")
    print("- Use appropriate alignment algorithms for your task")
    print("- Consider sequence quality and errors")
    print("- Use statistical methods for significance testing")
    print("- Consider computational complexity for large datasets")
    print("- Use standard databases for reference sequences")
    print("- Document your analysis pipeline")
    print("- Use appropriate genetic code for your organism")
    print("- Consider frame shifts and reading frames")
    print("- Validate gene predictions with experimental data")
    print("- Use appropriate statistical methods for motif finding")
    print("- Consider sequence annotation standards")


if __name__ == "__main__":
    demonstrate_bioinformatics()
