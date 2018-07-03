package edu.umb.cs.cs680.hw03;

import java.util.Objects;

public class DrawerClosedPlaying implements State {
	private DVDPlayer player;
	private DrawerClosedPlaying() {}
	private static DrawerClosedPlaying instance = null;
	
	public static DrawerClosedPlaying getInstance(){ // Singleton
		try{
		return Objects.requireNonNull(instance);
		}
		catch(NullPointerException ex){
		instance = new DrawerClosedPlaying();
		return instance;
		} }
	
	
	@Override
	public void openCloseButtonPushed() {
		player = DVDPlayer.getInstance();
		System.out.println("Open Button Pushed");
		player.stop();
		player.open();
		player.changeState(DrawerOpen.getInstance());
	
		
	}

	@Override
	public void playButtonPushed() {
		System.out.println("Play Button Pushed");
		System.out.println("Player Playing");

	}

	@Override
	public void stopButtonPushed() {
		System.out.println("Stop Button Pushed");
		System.out.println("Player Stopped");
		player = DVDPlayer.getInstance();
		player.changeState(DrawerClosedNotPlaying.getInstance());
		
	}

}
