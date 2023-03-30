-- submpv lua script
-- ===================|

local python_path = [[/bin/python]] -- path to python3 bin
local script_dir = mp.get_script_directory()
local utils = require 'mp.utils'

-- Log function: log to both terminal and MPV OSD (On-Screen Display)
function log(level,string,secs)
	secs = secs or 2.5
	mp.msg.log(level,string)
	mp.osd_message(string,secs)
end

-- download/load function
function submpv()
	log('info','searching for arabic subtitle!')
	--get directory and filename
	local directory,filename = utils.split_path(mp.get_property('path'))
	local table = { name = "subprocess",
			capture_stdout = true,
			args = { python_path }
			}
	local a = table.args

	a[#a + 1] = string.format("%s/submpv.py",script_dir)
	a[#a + 1] = '-d'
	a[#a + 1] = directory
	a[#a + 1] = filename --> submpv command ends with the movie/tvshow name/filename

	-- run command and capture stdout
	local result = mp.command_native(table)

	if result.status == 0 then
		if string.find(result.stdout, 'done') then
			log('info','Arabic subtitle ready!')
			-- to make sure all downloaded subtitle loaded
			mp.set_property('sub-auto', 'all')
			mp.commandv('rescan_external_files','reselect')
		else
			log('error','Arabic subtitles wasn\'t found!')
		end
	end
end
mp.add_key_binding(nil,'submpv',submpv)
