require 'ceedling'

ENV['COMPILER_ROOT'] = "C:/Program Files\ \(x86\)/Microchip/xc32/v2.10/"
#ENV['COMPILER_ROOT'] = "/opt/microchip/xc32/v2.10/"

Ceedling.load_project

task :default => %w[ clobber test:all gcov:all]