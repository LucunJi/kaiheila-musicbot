pulseaudio -D
pactl load-module module-null-sink sink_name=vspeaker sink_properties=device.description=virtual_speaker
pactl load-module module-remap-source master=vspeaker.monitor source_name=vmic source_properties=device.description=virtual_mic
pactl set-default-sink vspeaker
pactl set-default-source vmic
pactl list short sources
pactl list short sinks
