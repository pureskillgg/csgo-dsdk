

Documentation for CSDS files built by FPS Critic, Inc. 



## bomb_action - multi event
Events that trigger this channel: bomb_abort_plant, bomb_begin_plant, bomb_dropped, bomb_pickup, player_given_c4
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
event_type | replay | none | none |
player_id | replay | none | none |
site_code | replay | none | none |
entity_id | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## bomb_defuse - multi event
Events that trigger this channel: bomb_abort_defuse, bomb_begin_defuse
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
event_type | replay | none | none |
player_id | replay | none | none |
has_kit | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## bomb_state - multi event
Events that trigger this channel: bomb_defused, bomb_exploded, bomb_planted
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
event_type | replay | none | none |
player_id | replay | none | none |
site_code | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## bot_takeover - single event
Event that triggers this channel: bot_takeover
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
bot_id | replay | none | none |
player_index | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## grenade_state - multi event
Events that trigger this channel: decoy_detonate, decoy_firing, decoy_started, flashbang_detonate, hegrenade_detonate, smokegrenade_detonate, smokegrenade_expired
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
event_type | replay | none | none |
entity_id | replay | none | none |
player_id | replay | none | none |
x_pos | replay | none | none |
y_pos | replay | none | none |
z_pos | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
entity_id_fixed | calculated | round, entity_id, event_type, tick | none |
tick_throw | calculated | round, player_id, weapon_name, tick | none |
player_x_pos | merged | none | tick_throw, player_id |
player_y_pos | merged | none | tick_throw, player_id |
player_z_pos | merged | none | tick_throw, player_id |
player_x_vel | merged | none | tick_throw, player_id |
player_y_vel | merged | none | tick_throw, player_id |
player_z_vel | merged | none | tick_throw, player_id |
player_phi_ang | merged | none | tick_throw, player_id |
player_theta_ang | merged | none | tick_throw, player_id |
player_weapon_code | merged | none | tick_throw, player_id |
player_team_code | merged | none | tick_throw, player_id |


## header - header
Event that triggers this channel: none
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
magic | replay | none | none |
protocol | replay | none | none |
network_protocol | replay | none | none |
server_name | replay | none | none |
client_name | replay | none | none |
map_name | replay | none | none |
game_directory | replay | none | none |
playback_time | replay | none | none |
playback_ticks | replay | none | none |
playback_frames | replay | none | none |
signon_length | replay | none | none |
magic | replay | none | none |
protocol | replay | none | none |
network_protocol | replay | none | none |
server_name | replay | none | none |
client_name | replay | none | none |
map_name | replay | none | none |
game_directory | replay | none | none |
playback_time | replay | none | none |
playback_ticks | replay | none | none |
playback_frames | replay | none | none |
signon_length | replay | none | none |
tick_rate | calculated | playback_ticks, playback_time | none |
tick_save_rate | calculated | playback_frames, playback_time | none |
replay_version | calculated | meta:context.versions.replay | none |
match_date | calculated | meta:metadata.matchDate | none |
demo_id | calculated | meta:metadata.demoId | none |
sharecode | calculated | meta:metadata.sharecode | none |
platform | calculated | meta:metadata.platform | none |
match_type | calculated | meta:metadata.matchType | none |
second | calculated | tick, tick_rate | none |
t_starters_avg_rank | calculated | is_bot, round, rank, steam_id, team_code | none |
t_starters_avg_wins | calculated | is_bot, round, wins, steam_id, team_code | none |
ct_starters_avg_rank | calculated | is_bot, round, rank, steam_id, team_code | none |
ct_starters_avg_wins | calculated | is_bot, round, wins, steam_id, team_code | none |
ct_starters_score_final | calculated | round_state:ct_score | none |
t_starters_score_final | calculated | round_state:t_score | none |
number_of_points | calculated | shape of all data frames | none |


## item_equip - single event
Event that triggers this channel: item_equip
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
item | replay | none | none |
def_index | replay | none | none |
can_zoom | replay | none | none |
has_silencer | replay | none | none |
is_silenced | replay | none | none |
has_tracers | replay | none | none |
weapon_type_code | replay | none | none |
is_painted | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## item_pickup - single event
Event that triggers this channel: item_pickup
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
item | replay | none | none |
def_index | replay | none | none |
is_silent | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## item_remove - single event
Event that triggers this channel: item_remove
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
item | replay | none | none |
def_index | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## molotov_state - multi event
Events that trigger this channel: inferno_detonate, inferno_expire, inferno_extinguish, inferno_startburn
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
event_type | replay | none | none |
entity_id | replay | none | none |
x_pos | replay | none | none |
y_pos | replay | none | none |
z_pos | replay | none | none |
second | calculated | tick, tick_rate | none |
entity_id_fixed | calculated | round, entity_id, event_type, tick | none |
burn_duration | calculated | second, entity_id_fixed, event_type | none |
was_extinguished_by_smoke | calculated | second, entity_id_fixed, event_type, burn_duration | none |
extinguisher_id | calculated | second, entity_id_fixed, event_type, x_pos, y_pos, z_pos, player_id | none |
extinguisher_id_fixed | calculated | second, entity_id, entity_id_fixed, event_type, x_pos, y_pos, z_pos, player_id_fixed | none |
smoke_entity_id | calculated | second, entity_id, entity_id_fixed, event_type, x_pos, y_pos, z_pos | none |
was_extinguished_by_thrown_smoke | calculated | second, entity_id, entity_id_fixed, event_type, x_pos, y_pos, z_pos | none |
player_id | calculated | event_type, second, round | none |
player_id_fixed | calculated | event_type, second, round | none |
tick_throw | calculated | event_type, second, round | none |
player_x_pos | merged | none | tick_throw, player_id |
player_y_pos | merged | none | tick_throw, player_id |
player_z_pos | merged | none | tick_throw, player_id |
player_x_vel | merged | none | tick_throw, player_id |
player_y_vel | merged | none | tick_throw, player_id |
player_z_vel | merged | none | tick_throw, player_id |
player_phi_ang | merged | none | tick_throw, player_id |
player_theta_ang | merged | none | tick_throw, player_id |
player_weapon_code | merged | none | tick_throw, player_id |
player_team_code | merged | none | tick_throw, player_id |


## player_action - multi event
Events that trigger this channel: inspect_weapon, player_decal, player_jump, silencer_detach
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
event_type | replay | none | none |
player_id | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## player_blind - single event
Event that triggers this channel: player_blind
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
entity_id | replay | none | none |
attacker_id | replay | none | none |
blind_duration | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
attacker_id_fixed | merged | none | attacker_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |
attacker_x_pos | merged | none | attacker_id, tick |
attacker_y_pos | merged | none | attacker_id, tick |
attacker_z_pos | merged | none | attacker_id, tick |
attacker_x_vel | merged | none | attacker_id, tick |
attacker_y_vel | merged | none | attacker_id, tick |
attacker_z_vel | merged | none | attacker_id, tick |
attacker_phi_ang | merged | none | attacker_id, tick |
attacker_theta_ang | merged | none | attacker_id, tick |
attacker_weapon_code | merged | none | attacker_id, tick |
attacker_team_code | merged | none | attacker_id, tick |
attacker_tick | merged | none | attacker_id, tick |
attacker_player_id | merged | none | attacker_id, tick |


## player_connect - single event
Event that triggers this channel: player_connect
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_index | replay | none | none |
player_id | replay | none | none |
is_bot | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |


## player_death - single event
Event that triggers this channel: player_death
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
attacker_id | replay | none | none |
assister_id | replay | none | none |
weapon_name | replay | none | none |
is_headshot | replay | none | none |
penetration_amount | replay | none | none |
has_replay | replay | none | none |
is_flash_assist | replay | none | none |
is_through_smoke | replay | none | none |
is_attacker_blind | replay | none | none |
is_noscope | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
attacker_id_fixed | merged | none | attacker_id, round, steam_id |
assister_id_fixed | merged | none | assister_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |
attacker_x_pos | merged | none | attacker_id, tick |
attacker_y_pos | merged | none | attacker_id, tick |
attacker_z_pos | merged | none | attacker_id, tick |
attacker_x_vel | merged | none | attacker_id, tick |
attacker_y_vel | merged | none | attacker_id, tick |
attacker_z_vel | merged | none | attacker_id, tick |
attacker_phi_ang | merged | none | attacker_id, tick |
attacker_theta_ang | merged | none | attacker_id, tick |
attacker_weapon_code | merged | none | attacker_id, tick |
attacker_team_code | merged | none | attacker_id, tick |
attacker_tick | merged | none | attacker_id, tick |
attacker_player_id | merged | none | attacker_id, tick |
assister_x_pos | merged | none | assister_id, tick |
assister_y_pos | merged | none | assister_id, tick |
assister_z_pos | merged | none | assister_id, tick |
assister_x_vel | merged | none | assister_id, tick |
assister_y_vel | merged | none | assister_id, tick |
assister_z_vel | merged | none | assister_id, tick |
assister_phi_ang | merged | none | assister_id, tick |
assister_theta_ang | merged | none | assister_id, tick |
assister_weapon_code | merged | none | assister_id, tick |
assister_team_code | merged | none | assister_id, tick |
assister_tick | merged | none | assister_id, tick |
assister_player_id | merged | none | assister_id, tick |


## player_disconnect - single event
Event that triggers this channel: player_disconnect
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
disconnect_reason | replay | none | none |
is_bot | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |


## player_fall - single event
Event that triggers this channel: player_fall
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
damage | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## player_footstep - single event
Event that triggers this channel: player_footstep
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |


## player_hurt - single event
Event that triggers this channel: player_hurt
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
attacker_id | replay | none | none |
health | replay | none | none |
armor | replay | none | none |
weapon_name | replay | none | none |
health_removed | replay | none | none |
armor_removed | replay | none | none |
hit_box_code | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
attacker_id_fixed | merged | none | attacker_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |
attacker_x_pos | merged | none | attacker_id, tick |
attacker_y_pos | merged | none | attacker_id, tick |
attacker_z_pos | merged | none | attacker_id, tick |
attacker_x_vel | merged | none | attacker_id, tick |
attacker_y_vel | merged | none | attacker_id, tick |
attacker_z_vel | merged | none | attacker_id, tick |
attacker_phi_ang | merged | none | attacker_id, tick |
attacker_theta_ang | merged | none | attacker_id, tick |
attacker_weapon_code | merged | none | attacker_id, tick |
attacker_team_code | merged | none | attacker_id, tick |
attacker_tick | merged | none | attacker_id, tick |
attacker_player_id | merged | none | attacker_id, tick |
effective_health_removed | calculated | player_id, round, health | none |


## player_info - player info
Event that triggers this channel: round_freeze_end
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay-deleted | none | none |
player_id | replay | none | none |
team_code | replay | none | none |
wins | replay | none | none |
rank | replay | none | none |
commends_friendly | replay | none | none |
commends_leader | replay | none | none |
commends_teacher | replay | none | none |
radar_color_code | replay | none | none |
second | calculated-deleted | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |


## player_interaction - multi event
Events that trigger this channel: break_breakable, break_prop, door_moving, player_use
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
event_type | replay | none | none |
player_id | replay | none | none |
entity_id | replay | none | none |
material | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## player_name - single event
Event that triggers this channel: player_name
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
name_new | replay | none | none |
name_old | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |


## player_personal - player info
Event that triggers this channel: round_freeze_end
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay-deleted | none | none |
player_id | replay | none | none |
name | replay | none | none |
clan_tag | replay | none | none |
steam_id | replay | none | none |
second | calculated-deleted | tick, tick_rate | none |
is_bot | calculated | steam_id | none |
player_id_fixed | calculated | steam_id, is_bot | none |


## player_spawn - single event
Event that triggers this channel: player_spawn
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## player_status - telemetry
Event that triggers this channel: tick_end
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
tick | replay | none | none |
round | replay | none | none |
player_id | replay | none | none |
armor | replay | none | none |
health | replay | none | none |
place_name | replay | none | none |
inv_primary | replay | none | none |
inv_secondary | replay | none | none |
inv_flashbang | replay | none | none |
inv_taser | replay | none | none |
inv_hegrenade | replay | none | none |
inv_smokegrenade | replay | none | none |
inv_molotov | replay | none | none |
inv_decoy | replay | none | none |
inv_incgrenade | replay | none | none |
inv_c4 | replay | none | none |
current_equipment_cost | replay | none | none |
freezetime_end_equipment_cost | replay | none | none |
money | replay | none | none |
ping | replay | none | none |
round_start_equipment_cost | replay | none | none |
zoom_level | replay | none | none |
iron_sight_mode | replay | none | none |
burst_mode | replay | none | none |
is_silenced | replay | none | none |
reload_visually_complete | replay | none | none |
weapon_mode | replay | none | none |
flash_duration | replay | none | none |
flash_max_alpha | replay | none | none |
has_c4 | replay | none | none |
has_defuser | replay | none | none |
has_helmet | replay | none | none |
is_defusing | replay | none | none |
is_fake_player | replay | none | none |
is_in_bomb_zone | replay | none | none |
is_in_buy_zone | replay | none | none |
is_scoped | replay | none | none |
is_spotted | replay | none | none |
is_walking | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
equipment_value_calc | calculated | inv_flashbang, inv_taser, inv_hegrenade, inv_smokegrenade, inv_molotov, inv_decoy, inv_incgrenade, inv_c4, armor, has_defuser, has_helmet, inv_primary, inv_secondary | none |


## player_vector - telemetry
Event that triggers this channel: tick_end
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
tick | replay | none | none |
round | replay | none | none |
player_id | replay | none | none |
x_pos | replay | none | none |
y_pos | replay | none | none |
z_pos | replay | none | none |
x_vel | replay | none | none |
y_vel | replay | none | none |
z_vel | replay | none | none |
x_aimpunch | replay | none | none |
y_aimpunch | replay | none | none |
current_ammo | replay | none | none |
weapon_code | replay | none | none |
inaccuracy | replay | none | none |
last_shot_time | replay | none | none |
recoil_index | replay | none | none |
duck_amount | replay | none | none |
duck_speed | replay | none | none |
phi_ang | replay | none | none |
theta_ang | replay | none | none |
is_ducked | replay | none | none |
is_ducking | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
team_code | merged | none | round, player_id |
theta_vel | calculated | second, player_id, theta | none |
phi_vel | calculated | second, player_id, phi | none |
ang_vel | calculated | phi_vel, theta_vel | none |
speed_2d | calculated | x_vel, y_vel | none |
movement_angle | calculated | second, x_vel, y_vel | none |
movement_angle_diff | calculated | second, speed_2d, theta_ang, movement_angle | none |


## round_end - single event
Event that triggers this channel: round_end
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
winner_team_code | replay | none | none |
win_reason_code | replay | none | none |
win_reason_message | replay | none | none |
legacy_code | replay | none | none |
player_count | replay | none | none |
second | calculated | tick, tick_rate | none |


## round_mvp - single event
Event that triggers this channel: round_mvp
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
mvp_reason_code | replay | none | none |
music_kit_mvps | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |


## round_start - single event
Event that triggers this channel: round_start
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
time_limit | replay | none | none |
frag_limit | replay | none | none |
objective | replay | none | none |
second | calculated | tick, tick_rate | none |


## round_state - multi event
Events that trigger this channel: begin_new_match, bomb_defused, bomb_exploded, bomb_planted, buytime_ended, round_announce_match_start, round_announce_warmup, round_end, round_freeze_end, round_officially_ended, round_start, start_halftime
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
event_type | replay | none | none |
t_score | replay_fixed | none | none |
ct_score | replay_fixed | none | none |
t_score_raw | replay | none | none |
ct_score_raw | replay | none | none |
phase | replay | none | none |
is_warmup | replay | none | none |
second | calculated | tick, tick_rate | none |


## tick - single event
Event that triggers this channel: tick_end
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
second | calculated | tick, tick_rate | none |
previous_phase | calculated | event_type, second | none |
second_since_previous_phase | calculated | second | none |


## weapon_action - multi event
Events that trigger this channel: fire_on_empty, reload, zoom, zoom_rifle
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
event_type | replay | none | none |
player_id | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |


## weapon_fire - single event
Event that triggers this channel: weapon_fire
Col Name | Origin | Dependents | Merge Keys
--- | --- | --- | --- |
round | replay | none | none |
tick | replay | none | none |
player_id | replay | none | none |
weapon_name | replay | none | none |
is_silenced | replay | none | none |
second | calculated | tick, tick_rate | none |
player_id_fixed | merged | none | player_id, round, steam_id |
player_x_pos | merged | none | player_id, tick |
player_y_pos | merged | none | player_id, tick |
player_z_pos | merged | none | player_id, tick |
player_x_vel | merged | none | player_id, tick |
player_y_vel | merged | none | player_id, tick |
player_z_vel | merged | none | player_id, tick |
player_phi_ang | merged | none | player_id, tick |
player_theta_ang | merged | none | player_id, tick |
player_weapon_code | merged | none | player_id, tick |
player_team_code | merged | none | player_id, tick |
player_tick | merged | none | player_id, tick |
player_player_id | merged | none | player_id, tick |
missed_molotov | calculated | event_type-molotov_state, second-molotov_state | none |
