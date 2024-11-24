# iRacingBOT

This project aims tp create a Twitch bot for iRacing.

Currently this is an Alpha release both from a development and functionalities point of view, basically an MVP, looking for more experienced Python devs to join this project if interested.

Currently the application is setting the stream title based on the active iRacing session, the title will include session type and track, for example:

`Practice at Imola`

## Instruction for general users
Download the content of the `/output` folder:
- [authcode.html](output/authcode.html)
- [botwitch.exe](output/botwitch.exe)
- [iracingbot.exe](output/iracingbot.exe)

Make sure all files are in the same folder, execute `botwitch.exe` to generate a `data.json` file. Open the file and provide your Twitch channel name, i.e:
```
{
    "channel":"notechdrama,
    ...
}
```
Execute the `twitchbot.exe` file again and follow the instructions in your browser to authorize the bot with Twitch

You're now setup and can run `iracinbot.exe`, your Twitch stream title will change based on the active iRacing session.

You will need to ensure `iracingbot.exe` is always running, so you may want to add it to your startup login items.

## Instruction for devs
To be provided, feel free to reach out in github if interested.