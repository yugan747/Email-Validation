# Travelling Salesman Problem (TSP) Solver & Email Validation Django Project

## Project Overview

This repository contains two main components:

1. **Travelling Salesman Problem (TSP) Python Script**  
   - A Python script that calculates the **shortest possible route** for a salesman to visit all cities exactly once and return to the starting city.  
   - Uses a **brute-force approach** to find the minimum distance.  

2. **Email Validation API using Django & DRF**  
   - A REST API that validates emails for:  
     - Proper format  
     - MX records  
     - SPF, DKIM, and DMARC records  
     - SMTP verification  
   - Fully documented using **Swagger / Redoc**.

---

## Python Script: Shortest Route (TSP)

### Cities and Distances

The salesman must visit 6 cities: `A`, `B`, `C`, `D`, `E`, `F`.  
Distance matrix (in km):

| From/To | A  | B  | C  | D  | E  | F  |
|---------|----|----|----|----|----|----|
| A       | 0  | 10 | 15 | 20 | 25 | 30 |
| B       | 10 | 0  | 35 | 25 | 17 | 28 |
| C       | 15 | 35 | 0  | 30 | 28 | 40 |
| D       | 20 | 25 | 30 | 0  | 22 | 16 |
| E       | 25 | 17 | 28 | 22 | 0  | 35 |
| F       | 30 | 28 | 40 | 16 | 35 | 0  |

---

### How to Run the Script

1. Make sure you have **Python 3.x** installed.
2. Clone the repository:

```bash
git clone <repository_url>
cd <repository_folder>
