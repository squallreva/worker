from workers import WorkerEntrypoint, Response, URL
import random
import math

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Parse URL query params
        url = URL(request.url)
        nums_str = url.search_params.get('nums')
        if not nums_str:
            return Response.json({'error': 'Provide ?nums=a,b,c,d (e.g., 1,2,3,4)'}, status=400)
        
        try:
            digits = [float(x.strip()) for x in nums_str.split(',') if x.strip()]
            if len(digits) != 4:
                raise ValueError("Exactly 4 numbers required")
        except:
            return Response.json({'error': 'Invalid nums format'}, status=400)
        
        solutions = solve_24_game(digits)
        return Response.json({'solutions': solutions or ['No solution found']})

def solve_24_game(digits):
    # Recursive solver: Builds expressions by combining pairs
    arr = [{'val': digit, 'expr': str(digit)} for digit in digits]
    solutions = []
    
    def combo4(a, b, c, d):
        arr_local = [a, b, c, d]
        # Partial permutations to reduce search space
        permutations = [
            [0, 1, 2, 3], [0, 2, 1, 3], [0, 3, 1, 2],
            [1, 2, 0, 3], [1, 3, 0, 2], [2, 3, 0, 1]
        ]
        for perm in permutations:
            i, j, k, m = perm
            for combo in combos(arr_local[i], arr_local[j]):
                answer = combo3(combo, arr_local[k], arr_local[m])
                if answer:
                    solutions.append(answer)
    
    def combo3(a, b, c):
        arr_local = [a, b, c]
        permutations = [[0, 1, 2], [0, 2, 1], [1, 2, 0]]
        for perm in permutations:
            i, j, k = perm
            for combo in combos(arr_local[i], arr_local[j]):
                answer = combo2(combo, arr_local[k])
                if answer:
                    return answer
        return None
    
    def combo2(a, b):
        for combo in combos(a, b):
            if abs(combo['val'] - 24) < 1e-6:  # Floating-point tolerance
                return combo['expr']
        return None
    
    def combos(a, b):
        return [
            {'val': a['val'] + b['val'], 'expr': f"({a['expr']} + {b['expr']})"},
            {'val': a['val'] * b['val'], 'expr': f"({a['expr']} * {b['expr']})"},
            {'val': a['val'] - b['val'], 'expr': f"({a['expr']} - {b['expr']})"},
            {'val': b['val'] - a['val'], 'expr': f"({b['expr']} - {a['expr']})"},
            {'val': a['val'] / b['val'] if abs(b['val']) > 1e-6 else float('inf'), 'expr': f"({a['expr']} / {b['expr']})"},
            {'val': b['val'] / a['val'] if abs(a['val']) > 1e-6 else float('inf'), 'expr': f"({b['expr']} / {a['expr']})"},
        ]
    
    combo4(*arr)  # Run the solver
    return list(set(solutions))  # Deduplicate

# Optional: If no input, test with random digits (for dev)
if __name__ == "__main__":
    for _ in range(5):
        digits = [random.randint(1, 9) for _ in range(4)]
        print(f"{digits}: {solve_24_game(digits)}")
