# Portfolio Generator

This document was originally written in [English](https://github.com/lucsalm/portfolio-generator-dash/blob/main/README.md), but it is also available in [Portuguese](https://github.com/lucsalm/portfolio-generator-dash/blob/main/README-pt-BR.md).

## Overview

This project features an application designed around portfolio theory, offering users the ability to select up to three financial assets and specify the analysis period in years. Utilizing nonlinear optimization techniques on the Sharpe ratio, the application generates interactive dashboards that display detailed insights into the selected assets, including historical performance and asset allocation, as well as the expected return and risk of the portfolio.

## Example Screenshot:

![Portfolio Optimization Dashboard](https://raw.githubusercontent.com/lucsalm/portfolio-generator-dash/main/portfolio-example.png)

## Portfolio Theory:

Portfolio theory is one of the cornerstones of modern finance, focusing on optimizing asset allocation to maximize expected returns while minimizing associated risks. Introduced by Harry Markowitz in the 1950s, this theory revolutionized investment management by demonstrating the benefits of diversification, illustrating how a well-diversified portfolio can mitigate overall risk without sacrificing potential returns. For further exploration, refer to Markowitz's seminal paper: "Portfolio Selection" (Markowitz, H. (1952). Portfolio Selection. The Journal of Finance, 7(1), 77-91).

## How to Use:

1. Make sure Docker is installed on your machine.
2. Clone this repository to your local environment.
3. Navigate to the project directory.
4. In the terminal, execute the following command to build and start the Docker container:
    - On Linux, execute:
        ```bash
        docker compose up
        ```

    - On Windows, execute:
        ```bash
        docker-compose up
        ```

5. After the container is built and the application is initialized, access `http://localhost:8050` in your web browser to explore the Portfolio Optimization Dashboard.

**Note:** Ensure that port 8050 is not in use by any other application on your system to avoid conflicts. If necessary, you can modify the port mapping in the `docker-compose.yml` file.

## References:

- Markowitz, H. (1952). Portfolio Selection. The Journal of Finance, 7(1), 77-91.
