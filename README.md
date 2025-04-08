# Репозиторий с проектом по курсу "Процессы безопасной разработки ПО"
Выполнил студент 5 курса МФТИ, Кафдеры "Банковских и информационных технологий":
Цхай Александр


## Описание проекта
Проект состоит из фазинга проекта [grex](https://github.com/pemistahl/grex). В качетсве инструмента фазинга использовался libFuzz подобный [cargo-fuzz](https://rust-fuzz.github.io/book/cargo-fuzz.html).  
В репозитории в папке FirstFuzzing содержатся:
1. Директория [fuzz](/FirstFuzzing/fuzz), содержащая фазинг и покрытие
2. Директория [Hashing](/FirstFuzzing/Hashing) содержашая контрольный суммы файлов источников (и ещё приложил [скрипт](/FirstFuzzing/Hashing/script.py) которым их считал)

## Описание выполнения проекта
0. Создаем виртуалку Ubuntu (150 рублей в cloud.ru за публичный IP, а так бесплатно).
   1. Скачиваем туда gcc, g++, rust, cargo
   2. Качаем cargo-fuzz по [инструкции](https://rust-fuzz.github.io/book/cargo-fuzz/setup.html)
1. Скачиваем репозиторий для фазинга (в моем случае grex)
   1. Проверяем что проект собирается (делаем ```cargo build```)
2. Собираем чек-суммы фалов исходников (они лежат в папке src) с помощью написанного мной [скрипта](/FirstFuzzing/Hashing/script.py) (нужен модуль simple-file-checksum)
3. Фазить проект будем фазить как библиотеку, поэтому внутри репозитория выполняем команду
   ```shell-script
   cargo fuzz init
   ```
5. Создалась папка fuzz, а внутри нее fuzz_targets.
6. Внутри папки fuzz_targets лежит файл "fuzz_target_1.rs". В нем необходимо написать код которым будем фазить либу (аля entrypoint)
7. После того как написали заполнили кодом fuzz_target_1.rs можно запустить фазинг (я запустил примерно на 48 часов на виртуалке внутри монитора) командой:
   ```shell-script
   cargo fuzz run fuzz_target_1
   ```
8. После 48 часов работы видим что у нас накопился корпус в папке [fuzz/corpus](/FirstFuzzing/fuzz/corpus). И ещё были бы артефакты в директории fuzz/artifacts если бы я нашел падения но я их не нашел
9. Теперь сгенерируем покрытие на основе полученного корпуса.
   1. Предварительно нужно скачать llvm. Можно через сам rust:
      ```bash
      rustup component add --toolchain nightly llvm-tools-preview
      ```
   2. После этого запускаем покрытие:
      ```bash
      cargo fuzz coverage fuzz_target_1
      ```
10. Теперь сгенерируем report. После предыдущего шага появилась директория target (на том же уровне что и fuzz), в ней будет лежать бинарь скомпленный llvm'ом. Далее используем его для получения report'ов:
    ```bash
    ~/.rustup/toolchains/nightly-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/bin/llvm-cov show -instr-profile=fuzz/coverage/fuzz_target_1/coverage.profdata target/x86_64-unknown-linux-gnu/coverage/x86_64-unknown-linux-gnu/release/fuzz_target_1 -Xdemangler=rustfilt -ignore-filename-regex=\.cargo/registry -ignore-filename-regex=/rustc --format=html > index.html
    ```
    И
    ```bash
    ~/.rustup/toolchains/nightly-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/bin/llvm-cov report -instr-profile=fuzz/coverage/fuzz_target_1/coverage.profdata target/x86_64-unknown-linux-gnu/coverage/x86_64-unknown-linux-gnu/release/fuzz_target_1 -Xdemangler=rustfilt -ignore-filename-regex=\.cargo/registry -ignore-filename-regex=/rustc > report
    ```

Первая команда сгенерит [построчное покрытие](/FirstFuzzing/index.html), а вторая [общий report](/FirstFuzzing/report)
