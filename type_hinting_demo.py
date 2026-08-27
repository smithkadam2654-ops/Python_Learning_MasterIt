from typing import List, Dict, Optional, Union

def process_scores(scores: List[float], bonus: Optional[float] = None) -> Dict[str, Union[float, str]]:
    """
    Process a list of scores and return statistics.
    
    Args:
        scores: A list of floating point numbers.
        bonus: An optional bonus to add to every score.
        
    Returns:
        A dictionary containing the average and status.
    """
    if not scores:
        return {"average": 0.0, "status": "No scores provided"}
        
    if bonus is not None:
        scores = [s + bonus for s in scores]
        
    average = sum(scores) / len(scores)
    
    status = "Pass" if average >= 50.0 else "Fail"
    
    return {
        "average": average,
        "status": status
    }

def demonstrate_type_hinting():
    """Demonstrate functions with type hints."""
    # These hints help IDEs and tools like mypy catch errors!
    
    student_scores: List[float] = [45.5, 60.0, 30.5]
    
    result = process_scores(student_scores, bonus=5.0)
    
    print(f"Class average: {result['average']:.2f}")
    print(f"Overall status: {result['status']}")

if __name__ == "__main__":
    demonstrate_type_hinting()
