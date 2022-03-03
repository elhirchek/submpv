-- Log function: log to both terminal and MPV OSD (On-Screen Display)
function log(string,secs)
	secs = secs or 2.5
	mp.msg.warn(string)
	mp.osd_message(string,secs)
end

-- download/load function
function sub()
	log('search for arabic subtitle!')
	local utils = require 'mp.utils'
	--get directory and filename
	local d,f = utils.split_path(mp.get_property('path'))
	-- run command and capture stdout
	local openPop = assert(io.popen('/bin/python /home/usr/path/subscene_to_mpv.py -d '.. d ..' \''..f..'\'', 'r')) -- path to script
	local output = openPop:read('*all')
	openPop:close()
	-- check stdout 
	if string.find(output, 'done') then
		log('Arabic subtitles ready!')
		-- to make sure all downloaded subtitle loaded
		mp.set_property('sub-auto', 'all')
		mp.commandv('rescan_external_files','reselect')
	else
		log('Arabic subtitles not found!')
	end
end
mp.add_key_binding('g','sub',sub)
