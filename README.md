# HKCERT CTF 2020

## Folder structure

```
└── id-challengename/
  ├── public/                 contains the file available for user download
  ├── env/                    a dockerized environment that is accessible via `nc` or browsers
  │   ├── docker-compose.yml
  │   ├── image1/
  │   │   ├── Dockerfile
  │   │   └── ...
  │   └── image2/
  │       ├── Dockerfile
  │       └── ...
  ├── src/                    whatever files that is used as auxiliary to the challenge, in whatever
  │                           use. this includes but not limited to the source code for the binary,
  │                           the solution script (or writeup) that is considered to solve the
  │                           challenge.
  ├── writeups/
  │   ├── team1/
  │   │   └── README.md       the writeup and any auxiliary script that you used to solve a
  │   └── team2/              challenge - one folder per team.
  │       ├── README.md
  │       └── solve.py
  └── README.md               the README file that contains a brief summary (title, description,
                              category, author and flag) of the challenge
```
