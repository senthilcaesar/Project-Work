package edu.umb.cs.cs680.hw03;

import java.util.Objects;

public class DrawerClosedNotPlaying implements State  {
	private DVDPlayer player;
	DrawerClosedNotPlaying() {}
	private static DrawerClosedNotPlaying instance = null;
	
	public static DrawerClosedNotPlaying getInstance(){   // Singleton 
		try{
		return Objects.requireNonNull(instance);
		}
		catch(NullPointerException ex){
		instance = new DrawerClosedNotPlaying();
		
		return instance;
		} }
	
	@Override
	public void openCloseButtonPushed() {
	
		player = DVDPlayer.getInstance();
		System.out.println("Open Button Pushed");
		player.open();
		player.changeState(DrawerOpen.getInstance());
		
	}

	@Override
	public void playButtonPushed() {
		System.out.println("Play Button Pushed");
		System.out.println("Player Playing");
		player = DVDPlayer.getInstance();
		player.changeState(DrawerClosedPlaying.getInstance());
		
	}

	@Override
	public void stopButtonPushed() {
		System.out.println("Do Nothing");
		
	}

}
