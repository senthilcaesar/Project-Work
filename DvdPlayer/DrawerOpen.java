package edu.umb.cs.cs680.hw03;

import java.util.Objects;

public class DrawerOpen implements State {
	
	private DVDPlayer player;
	
	DrawerOpen() {}
	private static DrawerOpen instance = null;
	
	public static DrawerOpen getInstance(){ // Singleton
		try{
		return Objects.requireNonNull(instance);
		}
		catch(NullPointerException ex){
		instance = new DrawerOpen();
		return instance;
		} }
	
	@Override
	public void openCloseButtonPushed() {
		player = DVDPlayer.getInstance();
		System.out.println("Close Button Pushed");
		player.close();
		player.changeState(DrawerClosedNotPlaying.getInstance());
		
	}

	@Override
	public void playButtonPushed() {
		player = DVDPlayer.getInstance();
		System.out.println("Play Button Pushed");
		player.close();
		player.play();
		player.changeState(DrawerClosedPlaying.getInstance());
		
	}

	@Override
	public void stopButtonPushed() {
		System.out.println("Stop Button Pushed");
		System.out.println("Do Nothing");
		
	}

	
	
}
