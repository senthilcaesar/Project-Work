package edu.umb.cs.cs680.hw03;

import java.util.Objects;

public class DVDPlayer implements State {
	
	State playerState;
	
	private DVDPlayer() {}
	private static DVDPlayer player = null;
	
	public static DVDPlayer getInstance(){ // Singleton
		try{
		return Objects.requireNonNull(player);
		}
		catch(NullPointerException ex){
		player = new DVDPlayer();
		return player;
		} }
	
	public void changeState(State newState) {
		this.playerState = newState;
		}
	
	@Override
	public void openCloseButtonPushed() {
		playerState.openCloseButtonPushed();
		
	}

	@Override
	public void playButtonPushed() {
		playerState.playButtonPushed();
		
	}

	@Override
	public void stopButtonPushed() {
		playerState.stopButtonPushed();
		
	}
	
	public void open( ) {
		System.out.println("Drawer Opening");
	}

	public void close( ) {
		System.out.println("Drawer Closing");
	}
	
	public void play()  {
		System.out.println("Player Playing");
	}
	
	public void stop( ) {
		System.out.println("Player Stopped");
	}
	
	public State getState( ) {
		//return this.playerState.getClass().getName().substring(22);
		return this.playerState;
	}



}
