use std::collections::VecDeque;
use std::fs::File;
use std::io::{BufRead, BufReader};

type Error = Box<dyn std::error::Error>;

fn main() -> Result<(), Error> {
    let file = File::open("input/day01.txt")?;
    let reader = BufReader::new(file);
    let mut window = VecDeque::new();
    let mut result = 0;
    for line in reader.lines() {
        window.push_back(line?.parse::<i32>()?);
        if window.len() == 4 {
            if window.back() > window.front() {
                result += 1;
            }
            window.pop_front();
        }
    }
    println!("{} sums are larger", result);
    Ok(())
}
