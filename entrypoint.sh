# credits https://askubuntu.com/questions/1338747/virtual-audio-sink-virtual-audio-cable-on-ubuntu

echo "start PulseAudio deamon"
pulseaudio -D --exit-idle-time=-1

sleep 5

echo "setup virtual speaker and virtual miv"
pactl load-module module-null-sink sink_name=vspeaker sink_properties=device.description=virtual_speaker
pactl load-module module-remap-source master=vspeaker.monitor source_name=vmic source_properties=device.description=virtual_mic
pactl set-default-sink vspeaker
pactl set-default-source vmic
echo "show all sources"
pactl list short sources
echo "show all sinks"
pactl list short sinks

echo "run music bot"
python3 main.py &

echo "run default entrypoint"
/opt/bin/entry_point.sh
