# habitist ![habitist](https://github.com/amitness/habitist/workflows/habitist/badge.svg)
An automation to enable habit tracking in todoist. 

It integrates Seinfield's "[Don't Break the Chain](https://lifehacker.com/281626/jerry-seinfelds-productivity-secret)" method into [todoist](http://todoist.com/). Once it's setup, you can forget about it and it works seamlessly.  
<p align="center">
    <img src="https://i.imgur.com/PVp2TBs.png"/>
</p>

## Usage

![Habitist Screenshot](https://i.imgur.com/q4h2QGv.png)

1. You add habits you want to form as task on todoist with schedule `every day`

2. Add `[day 0]` to the task

3. When you complete the task, the [day 0] will become [day 1]

4. If you fail to complete the task and it becomes overdue, the script will schedule it to today and reset [day X] to [day 0].

## Setup Instructions
1. You will need a GitHub account to setup this for your use. Please signup from [here](https://github.com/join) if you don't have an account yet. 

2. Once logged in to GitHub, [fork](https://github.com/amitness/shuffle/fork) this repo to your GitHub account.  

![Forking a repo](https://i.imgur.com/2BDTiKR.png)

3. Find the Todoist API key for your account from `Settings > Integrations` from [here](https://todoist.com/prefs/integrations).  

![Setting up todoist key](https://i.imgur.com/sdCRpBI.png)

4. We want to trigger this once the day ends. So, you will need to find the time in UTC when it's 12 AM in your country.
> For example, Nepal is 5:45 hrs ahead of UTC. For 12:00 AM in Nepal, UTC time will be 6:15 pm i.e. 18:15.

You can use [https://www.thetimezoneconverter.com](https://www.thetimezoneconverter.com/) to do it. As seen in screenshot, you just need to type 00:00 in the local time and select the `24` hour button. Note the time you get in the UTC column.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
