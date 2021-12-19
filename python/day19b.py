from collections import deque
from dataclasses import dataclass
import io
from itertools import permutations, product
import numpy as np
import numpy.linalg as la

EXAMPLE = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""


Rotation = np.ndarray


def compute_rotations() -> list[Rotation]:
    rotations = []
    for (cols, signs) in product(permutations(range(3)), product([-1, 1], repeat=3)):
        rotation = np.zeros((3, 3))
        for i in range(3):
            rotation[i, cols[i]] = signs[i]
        if la.det(rotation) == 1:
            rotations.append(rotation)
    return rotations


ROTATIONS: list[Rotation] = compute_rotations()
assert len(ROTATIONS) == 24


Coord = np.ndarray


@dataclass
class Scanner:
    id: int
    beacons: list[Coord]
    position: Coord | None = None


def parse_input(reader: io.TextIOBase) -> list[Scanner]:
    scanners = []
    id = 0
    while reader.readline().startswith("---"):
        beacons = []
        while (line := reader.readline().strip()) != "":
            [x, y, z] = line.split(",")
            beacons.append(np.array([int(x), int(y), int(z)]))
        scanners.append(Scanner(id=id, beacons=beacons))
        id += 1
    return scanners


def match_pair(scanner1: Scanner, scanner2: Scanner) -> bool:
    assert scanner1.position is not None
    for rotation in ROTATIONS:
        beacons1 = scanner1.beacons
        beacons2 = [rotation @ beacon for beacon in scanner2.beacons]
        for (anchor1, anchor2) in product(beacons1, beacons2):
            deltas1 = {tuple(beacon - anchor1) for beacon in beacons1}
            deltas2 = {tuple(beacon - anchor2) for beacon in beacons2}
            if len(deltas1 & deltas2) >= 12:
                scanner2.beacons = beacons2
                scanner2.position = scanner1.position + anchor1 - anchor2
                return True
    return False


def match_list(scanners: list[Scanner]) -> None:
    scanners[0].position = np.zeros(3)
    queue = deque([scanners[0]])
    rest = scanners[1:]

    while len(queue) > 0:
        current = queue.popleft()
        old_rest = rest
        rest = []
        for scanner in old_rest:
            if match_pair(current, scanner):
                print(f"located scanner {scanner.id} at {scanner.position}")
                queue.append(scanner)
            else:
                rest.append(scanner)
    assert len(rest) == 0


scanners = parse_input(io.StringIO(EXAMPLE))
match_list(scanners)


def solve(reader: io.TextIOBase) -> int:
    scanners = parse_input(reader)
    match_list(scanners)
    return max(
        int(sum(abs(scanner1.position - scanner2.position)))
        for (scanner1, scanner2) in product(scanners, repeat=2)
    )


assert solve(io.StringIO(EXAMPLE)) == 3621


def main():
    with open("input/day19.txt") as file:
        result = solve(file)
        print(f"The biggest distance is {result}")


if __name__ == "__main__":
    main()
