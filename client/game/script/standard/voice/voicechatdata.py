human_commander_orders = OrderedDict([
	('Destroy the Enemy Lair' , {
		'Destroy the Enemy Lair' : 'sound/human/commander/destroy_lair_1.wav',
		'Destroy the Enemy Lair ' : 'sound/human/commander/destroy_lair_2.wav',
		'Destroy the Enemy Lair!' : 'sound/human/commander/destroy_lair_3.wav',
		'Destroy the Enemy Lair! ' : 'sound/human/commander/destroy_lair_4.wav'
	}),
	('Destroy the enemy Stronghold' , {
		'Destroy the enemy Stronghold' : 'sound/human/commander/destroy_stronghold_1.wav',
		'Destroy the enemy Stronghold ' : 'sound/human/commander/destroy_stronghold_2.wav',
		'Destroy the enemy Stronghold!' : 'sound/human/commander/destroy_stronghold_3.wav',
		'Destroy the enemy Stronghold! ' : 'sound/human/commander/destroy_stronghold_4.wav'
	}),
	('Capture the spawn flag' , {
		'Capture the Spawn Flag' : 'sound/human/commander/capture_flag_1.wav'
	}),
	('Return to base' , {
		'Return to base' : 'sound/human/commander/return_base_1.wav',
		 'Return to base!' : 'sound/human/commander/return_base_2.wav',
		 'Return to base ' : 'sound/human/commander/return_base_3.wav'
	}),
	('Scout for resources' , {
		'Scout for resources' : 'sound/human/commander/scout_resources_1.wav',
		'Scout for resources!' : 'sound/human/commander/scout_resources_2.wav',
		'Scout for resources ' : 'sound/human/commander/scout_resources_3.wav'
	}),
	('Scout for enemies' , {
		'Scout for enemies' : 'sound/human/commander/scout_enemies_1.wav',
		'Scout for enemies!' : 'sound/human/commander/scout_enemies_2.wav'
	}),
	('We need more gold' , {
		'We need more Gold' : 'sound/human/commander/need_gold_1.wav',
		'We need more Gold!' : 'sound/human/commander/need_gold_2.wav'
	}),
	('We need more redstone' , {
		'We need more Redstone' : 'sound/human/commander/need_redstone_1.wav',
		'We need more Redstone!' : 'sound/human/commander/need_redstone_2.wav'
	}),
	('Cancel orders' , {
		'Nevermind' : 'sound/human/commander/nevermind_1.wav',
		'Nevermind!' : 'sound/human/commander/nevermind_2.wav',
		'Disregard that order' : 'sound/human/commander/disregard_order_1.wav',
		'Disregard that order!' : 'sound/human/commander/disregard_order_2.wav'
	})
]);

human_commander_orders2 = OrderedDict([
	('Deploy landmines' , {
		'Deploy Landmines' : 'sound/human/commander/deploy_landmines_1.wav'
	}),
	('Deploy Sensors' , {
		'Deploy Sensors' : 'sound/human/commander/deploy_sensors_1.wav'
	}),
	('Clear the enemy Mine field' , {
		'Clear the enemy Mine field!' : 'sound/human/commander/clear_minefield_1.wav',
		'Clear the enemy Mine field' : 'sound/human/commander/clear_minefield_2.wav'
	}),
	('Clear the enemy Fire Wards' , {
		'Clear the enemy Fire Wards' : 'sound/human/commander/clear_firewards_1.wav',
		'Clear the enemy Fire Wards!' : 'sound/human/commander/clear_firewards_2.wav'
	}),
	('Reminder' , {
		'I gave you a command' : 'sound/human/commander/gave_command_1.wav',
		'Fool, obey my command' : 'sound/human/commander/fool_obey_1.wav',
		'Fool! Obey my command' : 'sound/human/commander/fool_obey_2.wav',
		'Obey my order' : 'sound/human/commander/obey_order_1.wav',
		'You must obey my order!' : 'sound/human/commander/must_obey_2.wav',
		'I gave you a command!' : 'sound/human/commander/gave_command_2.wav',
		'No... the other way!' : 'sound/human/commander/other_way_2.wav',
		'You must obey my order!' : 'sound/human/commander/must_obey_1.wav'
	})
]);

human_commander_misc = OrderedDict([
	('Thank you' , {
		'Thank you' : 'sound/human/commander/thank_you_1.wav',
		'Thank you ' : 'sound/human/commander/thank_you_1.wav',
		'Thank you!' : 'sound/human/commander/thank_you_2.wav'
	}),
	('Wait for my command!' , {
		'Wait for my command!' : 'sound/human/commander/wait_command_1.wav',
		'Wait for my command...' : 'sound/human/commander/wait_command_1.wav',
		'Wait for my command' : 'sound/human/commander/wait_command_2.wav'
	}),
	('Report your situation' , {
		'Report your situation' : 'sound/human/commander/report_situation_1.wav'
	}),
	('Well done' , {
		'Well done' : 'sound/human/commander/well_done_1.wav',
		'Well done!' : 'sound/human/commander/well_done_2.wav',
		'Excellent work' : 'sound/human/commander/well_done_3.wav',
		'Excellent work!' : 'sound/human/commander/well_done_4.wav'
	}),
	#TODO need commander voice rather than worker
	('We\'re being attacked!' , {
		'We\'re being attacked!' : 'sound/human/worker/being_attacked_2.wav',
		'We\'re being attacked!' : 'sound/human/worker/being_attacked_3.wav'
	})
]);

human_commander = OrderedDict([
	("General Orders", human_commander_orders),
	("More Orders", human_commander_orders2),
	("Misc Communication", human_commander_misc)
]);



beast_commander_orders = OrderedDict([
	('Destroy the Enemy Lair' , {
		'Destroy the Enemy Lair' : 'sound/beast/commander/destroy_lair_1.wav',
		'Destroy the Enemy Lair ' : 'sound/beast/commander/destroy_lair_2.wav',
		'Destroy the Enemy Lair!' : 'sound/beast/commander/destroy_lair_3.wav'
	}),
	('Destroy the enemy Stronghold' , {
		'Destroy the enemy Stronghold' : 'sound/beast/commander/destroy_stronghold_1.wav',
		'Destroy the enemy Stronghold ' : 'sound/beast/commander/destroy_stronghold_2.wav',
		'Destroy the enemy Stronghold!' : 'sound/beast/commander/destroy_stronghold_3.wav'
	}),
	('Capture the spawn flag' , {
		'Capture the Spawn Flag' : 'sound/beast/commander/capture_flag_1.wav',
		'Capture the Spawn Flag ' : 'sound/beast/commander/capture_flag_2.wav'
	}),
	('Return to base' , {
		'Return to base' : 'sound/beast/commander/return_base_1.wav',
		'Return to base ' : 'sound/beast/commander/return_base_2.wav',
		'Return to base!' : 'sound/beast/commander/return_base_3.wav'
	}),
	('Scout for resources' , {
		'Scout for resources' : 'sound/beast/commander/scout_resources_1.wav',
		'Scout for resources!' : 'sound/beast/commander/scout_resources_2.wav'
	}),
	('Scout for enemies' , {
		'Scout for enemies' : 'sound/beast/commander/scout_enemies_1.wav',
		'Scout for enemies ' : 'sound/beast/commander/scout_enemies_2.wav'
	}),
	('We need more gold' , {
		'We need more Gold' : 'sound/beast/commander/need_gold_1.wav',
		'We need more Gold ' : 'sound/beast/commander/need_gold_2.wav'
	}),
	('We need more redstone' , {
		'We need more Redstone' : 'sound/beast/commander/need_redstone_1.wav',
		'We need more Redstone ' : 'sound/beast/commander/need_redstone_2.wav'
	}),
	('Cancel orders' , {
		'Nevermind.' : 'sound/beast/commander/nevermind_1.wav',
		'Nevermind!' : 'sound/beast/commander/nevermind_2.wav',
		'Nevermind' : 'sound/beast/commander/nevermind_3.wav',
		'Disregard that order' : 'sound/beast/commander/disregard_order_1.wav',
		'Disregard that order!' : 'sound/beast/commander/disregard_order_2.wav'
	})
]);

beast_commander_orders2 = OrderedDict([
	('Deploy Fire Wards' , {
		'Deploy Fire Wards!' : 'sound/beast/commander/deploy_firewards_1.wav',
		'Deploy Fire Wards' : 'sound/beast/commander/deploy_firewards_2.wav'
	}),
	('Clear the enemy Mine field' , {
		'Clear the enemy Mine field' : 'sound/beast/commander/clear_minefield_1.wav',
		'Clear the enemy Mine field ' : 'sound/beast/commander/clear_minefield_2.wav'
	}),
	('Clear the enemy Fire Wards' , {
		'Clear the enemy Fire Wards!' : 'sound/beast/commander/clear_firewards_1.wav',
		'Clear the enemy Fire Wards' : 'sound/beast/commander/clear_firewards_2.wav'
	}),
	('Reminder' ,{
		'I gave you a command' : 'sound/beast/commander/gave_command_1.wav',
		'Fool, obey my command!' : 'sound/beast/commander/fool_obey_2.wav',
		'Fool, obey my command' : 'sound/beast/commander/fool_obey_1.wav',
		'Obey my order!' : 'sound/beast/commander/obey_order_1.wav',
		'Obey my order' : 'sound/beast/commander/obey_order_2.wav',
		'You must obey my order' : 'sound/beast/commander/must_obey_2.wav',
		'I gave you a command' : 'sound/beast/commander/gave_command_2.wav',
		'No... the other way!' : 'sound/beast/commander/other_way_2.wav',
		'You must obey my order!' : 'sound/beast/commander/must_obey_1.wav'
	}),
	#TODO use a commander, not worker voice
	('To battle!' , {
		'To battle!' : 'sound/beast/worker/to_battle_1.wav',
	})
]);

beast_commander_misc = OrderedDict([
	('Thank you' , {
		'Thank you' : 'sound/beast/commander/thank_you_1.wav',
		'Thank you ' : 'sound/beast/commander/thank_you_2.wav'
	}),
	('Wait for my command!' , {
		'Wait for my command!' : 'sound/beast/commander/wait_command_2.wav',
		'Wait for my command...' : 'sound/beast/commander/wait_command_1.wav',
		'Wait for my command!' : 'sound/beast/commander/wait_command_2.wav'
	}),
	('Report your situation' , {
		'Report your situation' : 'sound/beast/commander/report_situation_1.wav'
	}),
	('Well done' , {
		'Well done' : 'sound/beast/commander/well_done_1.wav',
		'Well done!' : 'sound/beast/commander/well_done_2.wav',
		'Well done ' : 'sound/beast/commander/well_done_3.wav',
		'Excellent work!' : 'sound/beast/commander/well_done_4.wav',
		'Excellent work' : 'sound/beast/commander/well_done_5.wav'
	}),
	#TODO use a comm and not worker voice
	('We\'re being attacked!' , {
		'We\'re being attacked' : 'sound/beast/worker/being_attacked_1.wav',
		'We\'re being attacked!' : 'sound/beast/worker/being_attacked_2.wav'
	}),
	('Depends on you' , {
		'The survival of the horde depends on you ' : 'sound/beast/commander/horde_depends_1.wav',
		'The survival of the horde depends on you' : 'sound/beast/commander/horde_depends_2.wav'
	})
]);

beast_commander = OrderedDict([
	("General Orders", beast_commander_orders),
	("More Orders", beast_commander_orders2),
	("Misc Communication", beast_commander_misc)
]);


human_player_male_observation = OrderedDict([
	('Creature spotted' , {
		'Creature spotted' : '/sound/human/player/male//creature_spotted_1.wav'
	}),
	('Resources spotted' , {
		'Resources spotted' : '/sound/human/player/male//resources_spotted_1.wav'
	}),
	('Enemy spotted' , {
		'Enemy spotted' : '/sound/human/player/male//enemy_spotted_1.wav',
		'Incoming enemies!' : '/sound/human/player/male//incoming_enemies_1.wav'
	}),
	('Enemy marksman spotted' , {
		'Enemy Marksman spotted' : '/sound/human/player/male//marksman_spotted_1.wav'
	}),
	('They have constructed a Garrison' , {
		'They have constructed a Garrison!' : '/sound/human/player/male//constructed_garrison_1.wav'
	}),
	('They have constructed a Sub Lair' , {
		'They have constructed a Sub Lair!' : '/sound/human/player/male//constructed_sublair_1.wav'
	}),
	('Enemy siege weapon spotted' , {
		'Enemy Siege Weapon spotted' : '/sound/human/player/male//siege_spotted_1.wav'
	}),
	('All clear' , {
		'All clear' : '/sound/human/player/male//all_clear_1.wav'
	}),
	('I need gold!' , {
		'I need gold!' : '/sound/human/player/male//need_gold_1.wav',
		'I need gold...' : '/sound/human/player/male//need_gold_2.wav',
		'I need gold' : '/sound/human/player/male//need_gold_3.wav'
	}),
	('I need this weapon!' , {
		'I need this weapon!' : '/sound/human/player/male//need_weapon_1.wav',
		'I need this weapon' : '/sound/human/player/male//need_weapon_2.wav'
	})
]);

human_player_male_basic = OrderedDict([
	('Your orders?' , {
		'Your orders?' : '/sound/human/player/male//your_orders_1.wav',
		'Your orders? ' : '/sound/human/player/male//your_orders_1.wav',
		'What is your order?' : '/sound/human/player/male//what_order_1.wav',
		'I need orders' : '/sound/human/player/male//need_orders_1.wav',
		'Give me your command!' : '/sound/human/player/male//give_command_1.wav'
	}),
	('Yes!' , {
		'Yes!' : '/sound/human/player/male//yes_1.wav',
		'Yes' : '/sound/human/player/male//yes_1.wav',
		'Yes! ' : '/sound/human/player/male//yes_2.wav',
		'Right away!' : '/sound/human/player/male//right_away_1.wav',
		'Absolutely!' : '/sound/human/player/male//absolutely_1.wav',
		'Command understood!' : '/sound/human/player/male//command_understood_1.wav',
		'With pleasure!' : '/sound/human/player/male//with_pleasure_1.wav',
		'With pleasure! ' : '/sound/human/player/male//with_pleasure_1.wav'
	}),
	('No!' , {
		'No!' : '/sound/human/player/male//no_1.wav',
		'Impossible!' : '/sound/human/player/male//impossible_1.wav'
	}),
	('Hello!' , {
		'Hello' : '/sound/human/player/male//hello_1.wav',
		'Hello!' : '/sound/human/player/male//hello_2.wav'
	}),
	('Thank you' , {
		'Thank you' : '/sound/human/player/male//thank_you_1.wav',
		'Thank you!' : '/sound/human/player/male//thank_you_2.wav'
	}),
	('Help!!!' , {
		'Help!!!' : '/sound/human/player/male//help_1.wav'
	}),
	('For the Legion' , {
		'For the Legion!' : '/sound/human/player/male//for_legion_1.wav',
		'Jaraziah is my leader' : '/sound/human/player/male//jaraziah_leader_1.wav'
	}),
	('I need a healer!' , {
		'I need healing!' : '/sound/human/player/male//need_healer_1.wav',
		'Please heal me!' : '/sound/human/player/male//need_healer_2.wav',
		'I need a Chaplain!' : '/sound/human/player/male//need_healer_3.wav'
	}),
	('I need a powerup!' , {
		'I need a powerup!' : '/sound/human/player/male//need_powerup_1.wav'
	}),
	('I\'m on my way!' , {
		'I\'m on my way!' : '/sound/human/player/male//on_way_1.wav'
	})
]);

human_player_male_tactics = OrderedDict([
	('Attack my target' , {
		'Attack!' : '/sound/human/player/male//attack_1.wav',
		'Attack my target' : '/sound/human/player/male//attack_here_4.wav',
		'Attack my target ' : '/sound/human/player/male//attack_here_4.wav'
	}),
	('Move!' , {
		'Move!' : '/sound/human/player/male//move_1.wav'
	}),
	('Follow me!' , {
		'Follow me!' : '/sound/human/player/male//follow_me_1.wav'
	}),
	('Cover me!' , {
		'Cover me!' : '/sound/human/player/male//cover_me_1.wav'
	}),
	('Capture the spawn flag' , {
		'Capture the spawn flag' : '/sound/human/player/male//capture_flag_1.wav'
	}),
	('Wait here for reinforcements' , {
		'Wait here for reinforcements' : '/sound/human/player/male//wait_reinforcements_1.wav',
		'Wait here for reinforcements ' : '/sound/human/player/male//wait_reinforcements_1.wav',
		'Hold position!' : '/sound/human/player/male//hold_position_1.wav'
	}),
	('Your orders?' , {
		'Your orders?' : '/sound/human/player/male//your_orders_1.wav',
		'What is your order?' : '/sound/human/player/male//what_order_1.wav',
		'I need orders' : '/sound/human/player/male//need_orders_1.wav',
		'Give me your command!' : '/sound/human/player/male//give_command_1.wav'
	}),
	('Be careful!' , {
		'Be careful!' : '/sound/human/player/male//be_careful_1.wav'
	}),
	('Spread out!' , {
		'Spread out!' : '/sound/human/player/male//spread_out_1.wav'
	}),
	('Retreat!' , {
		'Retreat!' : '/sound/human/player/male//retreat_1.wav'
	})
]);

human_player_male_offense = OrderedDict([
	('I\'m fighting on offense' , {
		'I\'m fighting on offense' : '/sound/human/player/male//im_offense_1.wav'
	}),
	('Attack!' , {
		'Attack!' : '/sound/human/player/male//attack_1.wav'
	}),
	('Charge!!' , {
		'Charge!!' : '/sound/human/player/male//charge_1.wav'
	}),
	('Attack their workers!' , {
		'Attack their Workers!' : '/sound/human/player/male//attack_workers_1.wav'
	}),
	('Attack the enemy Stronghold' , {
		'Attack the enemy Stronghold' : '/sound/human/player/male//attack_stronghold_1.wav'
	}),
	('Attack the enemy Lair' , {
		'Attack the enemy Lair' : '/sound/human/player/male//attack_lair_1.wav'
	}),
	('Attack the enemy structure' , {
		'Attack the enemy structure' : '/sound/human/player/male//attack_structure_1.wav'
	}),
	('Protect the Siege Units' , {
		'Protect the Siege units' : '/sound/human/player/male//protect_siege_1.wav'
	}),
	('Protect the Officer' , {
		'Protect the Officer' : '/sound/human/player/male//protect_officer_1.wav'
	}),
	('Build a Garrison here!' , {
		'Build a Garrison here!' : '/sound/human/player/male//build_garrison_1.wav'
	})
]);

human_player_male_defense = OrderedDict([
	('I\'m on defense' , {
		'I\'m on defense' : '/sound/human/player/male//im_defense_1.wav'
	}),
	('Defend the Stronghold' , {
		'Defend the Stronghold' : '/sound/human/player/male//defend_stronghold_1.wav'
	}),
	('Defend this structure' , {
		'Defend this structure' : '/sound/human/player/male//defend_structure_1.wav'
	}),
	('Defend this mine' , {
		'Defend this Mine' : '/sound/human/player/male//defend_mine_1.wav'
	}),
	('Protect the workers' , {
		'Protect the Workers' : '/sound/human/player/male//protect_workers_1.wav'
	}),
	('Our workers are under attack!' , {
		'Our workers are under attack!' : '/sound/human/player/male//workers_attack_1.wav'
	}),
	('Build defenses here' , {
		'Build defenses here' : '/sound/human/player/male//build_defenses_1.wav'
	}),
	('Enemy in our base' , {
		'Enemy in our base' : '/sound/human/player/male//enemy_base_1.wav',
		'Our base is overrun' : '/sound/human/player/male//base_overrun_1.wav'
	}),
	('Incoming siege!' , {
		'Incoming siege!' : '/sound/human/player/male//incoming_siege_1.wav'
	}),
	('Base is secure' , {
		'Base is secure' : '/sound/human/player/male//base_secure_1.wav'
	})
]);

human_player_male_battle_report = OrderedDict([
	('We have destroyed the enemy structure' , {
		'We have destroyed the enemy structure' : '/sound/human/player/male//destroyed_structure_1.wav'
	}),
	('We are attacking their Garrison' , {
		'We are attacking their Garrison!' : '/sound/human/player/male//attacking_garrison_1.wav'
	}),
	('We are attacking their Sub Lair' , {
		'We are attacking their Sub Lair!' : '/sound/human/player/male//attacking_sublair_1.wav'
	}),
	('We are damaging their Stronghold' , {
		'We are damaging their Stronghold!' : '/sound/human/player/male//damaging_stronghold_1.wav'
	}),
	('We are damaging their Lair!' , {
		'We are damaging their Lair!' : '/sound/human/player/male//damaging_lair_1.wav'
	}),
	('Their Stronghold is burning!' , {
		'Their Stronghold is burning!' : '/sound/human/player/male//stronghold_burning_1.wav'
	}),
	('Their Lair is burning!' , {
		'Their Lair is burning!' : '/sound/human/player/male//lair_burning_1.wav'
	}),
	('Their Stronghold is nearly destroyed' , {
		'Their Stronghold is nearly destroyed!' : '/sound/human/player/male//stronghold_nearly_destroyed_1.wav'
	}),
	('Their Lair is nearly destroyed!' , {
		'Their Lair is nearly destroyed!' : '/sound/human/player/male//lair_nearly_destroyed_1.wav'
	})
]);

human_player_male_global = OrderedDict([
	('Cower!' , {
		'Cower before the might of the Legion' : '/sound/human/player/male//cower_legion_1.wav'
	}),
	('Yes!' , {
		'Yes ' : '/sound/human/player/male//yes_1.wav',
		'Yes' : '/sound/human/player/male//yes_1.wav',
		'Yes!' : '/sound/human/player/male//yes_2.wav',
		'Absolutely!' : '/sound/human/player/male//absolutely_1.wav'
	}),
	('No!' , {
		'No!' : '/sound/human/player/male//no_1.wav'
	}),
	('Hello!' , {
		'Hello' : '/sound/human/player/male//hello_1.wav',
		'Hello!' : '/sound/human/player/male//hello_2.wav'
	}),
	('Thank you' , {
		'Thank you' : '/sound/human/player/male//thank_you_1.wav'
	}),
	('Good game' , {
		'Good game' : '/sound/human/player/male//good_game_1.wav',
		'Good game ' : '/sound/human/player/male//good_game_2.wav',
		'Good game!' : '/sound/human/player/male//good_game_3.wav'
	}),
	('For the Legion' , {
		'For the Legion!' : '/sound/human/player/male//for_legion_1.wav',
		'Jaraziah is my leader' : '/sound/human/player/male//jaraziah_leader_1.wav'
	}),
	('Good-bye' , {
		'Good-bye!' : '/sound/human/player/male/goodbye_1.wav'
	})
]);


human_player_male = OrderedDict([
	("Observation", human_player_male_observation),
	("Basic", human_player_male_basic),
	("Tactics", human_player_male_tactics),
	("Offense", human_player_male_offense),
	("Defense", human_player_male_defense),
	("Battle Report", human_player_male_battle_report),
	("Global", human_player_male_global)
]);

beast_player_male_observation = OrderedDict([
	('Creature spotted' , {
		'Creature spotted' : '/sound/beast/player/male//creature_spotted_1.wav'
	}),
	('Resources spotted' , {
		'Resources spotted' : '/sound/beast/player/male//resources_spotted_1.wav'
	}),
	('Enemy spotted' , {
		'Enemy spotted' : '/sound/beast/player/male//enemy_spotted_1.wav',
		'Incoming enemies!' : '/sound/beast/player/male//incoming_enemies_1.wav'
	}),
	('Enemy marksman spotted' , {
		'Enemy marksman spotted' : '/sound/beast/player/male//marksman_spotted_1.wav'
	}),
	('They have constructed a Garrison' , {
		'They have constructed a Garrison!' : '/sound/beast/player/male//constructed_garrison_1.wav'
	}),
	('They have constructed a Sub Lair' , {
		'They have constructed a Sub Lair!' : '/sound/beast/player/male//constructed_sublair_1.wav'
	}),
	('Enemy Siege weapon spotted' , {
		'Enemy Siege weapon spotted' : '/sound/beast/player/male//siege_spotted_1.wav'
	}),
	('All clear' , {
		'All clear' : '/sound/beast/player/male//all_clear_1.wav'
	}),
	('I need gold!' , {
		'I need gold!' : '/sound/beast/player/male//need_gold_1.wav'
	}),
	('I need this weapon!' , {
		'I need this weapon ' : '/sound/beast/player/male//need_weapon_1.wav',
		'I need this weapon!' : '/sound/beast/player/male//need_weapon_2.wav'
	})
]);

beast_player_male_basic = OrderedDict([
	('Your orders?' , {
		'Your orders?' : '/sound/beast/player/male//your_orders_1.wav',
		'I need orders' : '/sound/beast/player/male//need_orders_1.wav',
		'Give me your command!' : '/sound/beast/player/male//give_command_1.wav'
	}),
	('Yes!' , {
		'Yes!' : '/sound/beast/player/male//yes_1.wav',
		'Yes.' : '/sound/beast/player/male//yes_reply_1.wav',
		'Right away!' : '/sound/beast/player/male//right_away_1.wav',
		'Absolutely!' : '/sound/beast/player/male//absolutely_1.wav',
		'Command understood!' : '/sound/beast/player/male//command_understood_1.wav',
		'With pleasure! ' : '/sound/beast/player/male//with_pleasure_1.wav',
		'Yes! ' : '/sound/beast/player/male//yes_1.wav',
		'With pleasure!' : '/sound/beast/player/male//with_pleasure_1.wav'
	}),
	('No!' , {
		'No ' : '/sound/beast/player/male//no_1.wav',
		'Impossible!' : '/sound/beast/player/male//impossible_1.wav',
		'No' : '/sound/beast/player/male//no_1.wav',
		'No!' : '/sound/beast/player/male//no_2.wav'
	}),
	('Hello!' , {
		'Hello' : '/sound/beast/player/male//hello_1.wav',
		'Hello!' : '/sound/beast/player/male//hello_2.wav'
	}),
	('Thank you' , {
		'Thank you' : '/sound/beast/player/male//thank_you_1.wav'
	}),
	('Help!!!' , {
		'Help!!!' : '/sound/beast/player/male//help_1.wav'
	}),
	('For the Horde' , {
		'For the Horde!' : '/sound/beast/player/male//for_horde_1.wav',
		'Ophelia is my leader' : '/sound/beast/player/male//ophelia_leader_1.wav'
	}),
	('I need a shaman!' , {
		'I need a shaman!' : '/sound/beast/player/male//need_healer_1.wav',
		'I am injured!' : '/sound/beast/player/male//need_healer_2.wav',
		'Please heal me!' : '/sound/beast/player/male//need_healer_3.wav'
	}),
	('I need a powerup!' , {
		'I need a powerup!' : '/sound/beast/player/male//need_powerup_1.wav'
	}),
	('I understand' , {
		'I understand' : '/sound/beast/player/male//1_understand_1.wav'
	})
]);

beast_player_male_tactics = OrderedDict([
	('Attack my target' , {
		'Attack my target' : '/sound/beast/player/male//attack_target_1.wav',
		'Attack!' : '/sound/beast/player/male//attack_1.wav',
		'Attack my target' : '/sound/beast/player/male//attack_target_1.wav'
	}),
	('Move!' , {
		'Move!' : '/sound/beast/player/male//move_1.wav'
	}),
	('Follow me!' , {
		'Follow me!' : '/sound/beast/player/male//follow_me_1.wav'
	}),
	('Cover me!' , {
		'Cover me!' : '/sound/beast/player/male//cover_me_1.wav'
	}),
	('Capture the spawn flag' , {
		'Capture the spawn flag' : '/sound/beast/player/male//capture_flag_1.wav'
	}),
	('Wait here for reinforcements' , {
		'Wait here for reinforcements' : '/sound/beast/player/male//wait_reinforcements_1.wav'
	}),
	('Your orders?' , {
		'Your orders?' : '/sound/beast/player/male//your_orders_1.wav',
		'Your orders? ' : '/sound/beast/player/male//your_orders_1.wav',
		'I need orders' : '/sound/beast/player/male//need_orders_1.wav',
		'Give me your command!' : '/sound/beast/player/male//give_command_1.wav'
	}),
	('Be careful!' , {
		'Be careful!' : '/sound/beast/player/male//be_careful_1.wav'
	}),
	('Spread out!' , {
		'Spread out!' : '/sound/beast/player/male//spread_out_1.wav'
	}),
	('Retreat!' , {
		'Retreat!' : '/sound/beast/player/male//retreat_1.wav'
	})
]);

beast_player_male_offense = OrderedDict([
	('I\'m fighting on offense' , {
		'I\'m fighting on offense' : '/sound/beast/player/male//im_offense_1.wav'
	}),
	('Attack!' , {
		'Attack!' : '/sound/beast/player/male//attack_1.wav'
	}),
	('Charge!!' , {
		'Charge!!' : '/sound/beast/player/male//charge_1.wav'
	}),
	('Attack their workers!' , {
		'Attack their workers!' : '/sound/beast/player/male//attack_workers_1.wav'
	}),
	('Attack the enemy Stronghold' , {
		'Attack the enemy Stronghold' : '/sound/beast/player/male//attack_stronghold_1.wav'
	}),
	('Attack the enemy Lair' , {
		'Attack the enemy Lair' : '/sound/beast/player/male//attack_lair_1.wav'
	}),
	('Attack the enemy structure' , {
		'Attack the enemy structure' : '/sound/beast/player/male//attack_structure_1.wav'
	}),
	('Protect the siege units' , {
		'Protect the Siege units' : '/sound/beast/player/male//protect_siege_1.wav'
	}),
	('Protect the officer' , {
		'Protect the Officer' : '/sound/beast/player/male//protect_officer_1.wav'
	}),
	('Build a Sub Lair here' , {
		'Build a Sub Lair here' : '/sound/beast/player/male//build_sublair_1.wav'
	})
]);

beast_player_male_defense = OrderedDict([
	('I\'m on defense' , {
		'I\'m on defense' : '/sound/beast/player/male//im_defense_1.wav'
	}),
	('Defend the Lair' , {
		'Defend the Lair' : '/sound/beast/player/male//defend_lair_1.wav'
	}),
	('Defend this structure' , {
		'Defend this structure' : '/sound/beast/player/male//defend_structure_1.wav'
	}),
	('Defend this mine' , {
		'Defend this mine' : '/sound/beast/player/male//defend_mine_1.wav'
	}),
	('Protect the workers' , {
		'Protect the workers' : '/sound/beast/player/male//protect_workers_1.wav'
	}),
	('Our workers are under attack!' , {
		'Our workers are under attack!' : '/sound/beast/player/male//workers_attack_1.wav'
	}),
	('Build defenses here' , {
		'Build defenses here' : '/sound/beast/player/male//build_defenses_1.wav'
	}),
	('Enemy in our base' , {
		'Enemy in our base' : '/sound/beast/player/male//enemy_base_1.wav',
		'Our base is overrun' : '/sound/beast/player/male//base_overrun_1.wav'
	}),
	('Incoming siege!' , {
		'Incoming siege!' : '/sound/beast/player/male//incoming_siege_1.wav'
	}),
	('Base is secure' , {
		'Base is secure' : '/sound/beast/player/male//base_secure_1.wav'
	})
]);

beast_player_male_battle_report = OrderedDict([
	('We have destroyed the enemy structure' , {
		'We have destroyed the enemy structure' : '/sound/beast/player/male//destroyed_structure_1.wav'
	}),
	('We are attacking their Garrison' , {
		'We are attacking their Garrison!' : '/sound/beast/player/male//attacking_garrison_1.wav'
	}),
	('We are attacking their Sub Lair' , {
		'We are attacking their Sub Lair!' : '/sound/beast/player/male//attacking_sublair_1.wav'
	}),
	('We are damaging their Stronghold' , {
		'We are damaging their Stronghold!' : '/sound/beast/player/male//damaging_stronghold_1.wav'
	}),
	('We are damaging their Lair!' , {
		'We are damaging their Lair!' : '/sound/beast/player/male//damaging_lair_1.wav'
	}),
	('Their Stronghold is burning!' , {
		'Their Stronghold is burning!' : '/sound/beast/player/male//stronghold_burning_1.wav'
	}),
	('Their Lair is burning!' , {
		'Their Lair is burning!' : '/sound/beast/player/male//lair_burning_1.wav'
	}),
	('Their stronghold is nearly destroyed' , {
		'Their stronghold is nearly destroyed!' : '/sound/beast/player/male//stronghold_nearly_destroyed_1.wav'
	}),
	('Their Lair is nearly destroyed!' , {
		'Their Lair is nearly destroyed!' : '/sound/beast/player/male//lair_nearly_destroyed_1.wav'
	})
]);

beast_player_male_global = OrderedDict([
	('Strength of the Horde' , {
		'Now you know the strength of the Horde' : '/sound/beast/player/male//horde_strength_1.wav'
	}),
	('Yes!' , {
		'Yes!' : '/sound/beast/player/male//yes_1.wav',
		'Yes!' : '/sound/beast/player/male//yes_1.wav',
		'Yes.' : '/sound/beast/player/male//yes_reply_1.wav',
		'Absolutely!' : '/sound/beast/player/male//absolutely_1.wav'
	}),
	('No!' , {
		'No!' : '/sound/beast/player/male//no_1.wav',
		'No!' : '/sound/beast/player/male//no_2.wav',
		'No!' : '/sound/beast/player/male//no_1.wav'
	}),
	('Hello!' , {
		'Hello!' : '/sound/beast/player/male//hello_1.wav',
		'Hello!' : '/sound/beast/player/male//hello_2.wav'
	}),
	('Thank you' , {
		'Thank you' : '/sound/beast/player/male//thank_you_1.wav'
	}),
	('Good game' , {
		'Good game' : '/sound/beast/player/male//good_game_1.wav'
	}),
	('For the Horde' , {
		'For the Horde!' : '/sound/beast/player/male//for_horde_1.wav',
		'Ophelia is my leader' : '/sound/beast/player/male//ophelia_leader_1.wav'
	}),
	('Good-bye' , {
		'Good-bye!' : '/sound/beast/player/male/goodbye_1.wav',
		'Good-bye!' : '/sound/beast/player/male/goodbye_2.wav'
	})
]);


beast_player_male = OrderedDict([
	("Observation", beast_player_male_observation),
	("Basic", beast_player_male_basic),
	("Tactics", beast_player_male_tactics),
	("Offense", beast_player_male_offense),
	("Defense", beast_player_male_defense),
	("Battle Report", beast_player_male_battle_report),
	("Global", beast_player_male_global)
]);
