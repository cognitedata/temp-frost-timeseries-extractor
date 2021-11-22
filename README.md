# Frost API Timeseries Extractor

This is a part of SA Onboarding tasks:

> Create an extractor with extractor-utils to get the temperature  (in °C) of a location of your choice as a timeseries datapoints directly to CDF (Frost Met api)


1. Installation
    ```shell
    poetry install
    ```

2. Set following env variables:
    - **CLIENT_ID**: this is client id related to the App registered in Azure Active Directory
    - **CLIENT_SECRET**: same as **CLIENT_ID**
    - **TENANT**: same as previous
    - **TOKEN_URL**: same as previous
    - **PIPELINE_ID**: external id of extractor pipeline configured in CDF
    - **FROST_CLIENT_ID**: this is client id which is recived upon registration to [Frost API](https://frost.met.no/index.html)
    - **TIMESERIES_ID**: timeseries id from CDF to which datapoints will be pushed
    - **SENSORY_SYSTEM_ID**: SN ID from Frost API
    - **VARIABLE**: variable, i.e. elementID, from Frost API for which data points are fetched
    - **TIME_RES**: time resolution for data points in ISO8601 format (e.g., PT1H -> hourly values)
    - **VALID_FROM**: initial date/time from which onwards data points will be fetched (e.g., *2021-10-01T00:00:00*)


3. As an alternative to Step 2, one can add values directly in [config.yaml](./config.yaml) for relevant entries instead of providing them as env variables.

4. Run extractor:
    ```shell
    poetry run frost_locations config.yaml
    ```


## Docker image

All the necessary configs and shell scripts for creation od docker image are located in [docker-env](./docker-env) folder. These are:

- **Dockerfile**: a recepie for building docker image
- **extractor-crontab**: cron job config which sets docker container to execute `extractor.sh` to run every 6 hours (if new to cron, use [cron guru](https://crontab.guru/) to generate desired frequency of execution of targeted job)
- **extractor.sh**: shell script which calls `frost_ts` extractor

### Docker image creation
To create docker image do following:
1. Clone this repository
2. Update [config.yaml](./config.yaml) with required parameters (check the previous section of README.md)
3. Modify [extractor-crontab](./docker-env/extractor-crontab) if needed (e.g., to update frequency of cron job)
3. Use terminal and cd into the folder that was created when cloning the repository, and where [config.yaml](./config.yaml)
4. Execute the following command:
```shell
 docker build -t frost-ts-extractor -f docker-env/Dockerfile .
 ```
