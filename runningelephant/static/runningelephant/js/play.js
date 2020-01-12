
game.PlayScreen = me.ScreenObject.extend({
	/**	
	 *  action to perform on state change
	 */
	onResetEvent: function() {	
		
		// play the audio track
		me.audio.playTrack("dst-inertexponent");
		
        // load a level
		me.levelDirector.loadLevel("area01");
		
		// reset the score
		game.data.score = 0;
		
		// add our HUD to the game world
		this.HUD = new game.HUD.Container();
		me.game.world.addChild(this.HUD);
		me.audio.play("start");
	},
	
	/**	
	 *  action to perform when leaving this screen (state change)
	 */
	onDestroyEvent: function() {
		// remove the HUD from the game world
		me.game.world.removeChild(this.HUD);
	}
});


