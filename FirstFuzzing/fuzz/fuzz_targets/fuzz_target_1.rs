#![no_main]

use libfuzzer_sys::fuzz_target;
use grex::RegExpBuilder;

fuzz_target!(|data: &[u8]| {
    if data.len() > 4096 {
        return;
    }

    if let Ok(s) = std::str::from_utf8(data) {
        let inputs: Vec<&str> = s.lines().collect();

        if !inputs.is_empty() {
            let _ = RegExpBuilder::from(&inputs).build();
        }
    }
});
