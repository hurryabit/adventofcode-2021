use std::fs::File;
use std::io::{BufRead, BufReader};

type Error = Box<dyn std::error::Error>;

fn main() -> Result<(), Error> {
    let file = File::open("input/day01.txt")?;
    let reader = BufReader::new(file);
    let mut last = i32::MAX;
    let mut result = 0;
    for line in reader.lines() {
        let current = line?.parse::<i32>()?;
        if current > last {
            result += 1;
        }
        last = current;
    }
    println!("{} measurements are larger", result);
    Ok(())
}
