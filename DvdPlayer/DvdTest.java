package edu.umb.cs.cs680.hw03;

import static org.junit.Assert.*;
import org.junit.Test;
import static org.hamcrest.CoreMatchers.*;

public class DvdTest {


    private DVDPlayer player = DVDPlayer.getInstance();
	
    @Test
	public void DrawerInstanceTest() {
		
    	player.changeState(DrawerClosedNotPlaying.getInstance());
        State expectedState = DrawerClosedNotPlaying.getInstance();
    	State actualState = player.getState();
    	assertThat(actualState, is(sameInstance(expectedState)));
    	
    }
    @Test
    public void openCloseButtonPushedTest() {
    	player.changeState(DrawerClosedNotPlaying.getInstance());
       	player.openCloseButtonPushed();
    	State actualState = player.getState();
    	State expectedState = DrawerOpen.getInstance();
    	assertThat(actualState, is(sameInstance(expectedState)));
    	
    }
    @Test
    public void playButtonPushedTest() {
    	player.changeState(DrawerOpen.getInstance());
       	player.playButtonPushed();
    	State actualState = player.getState();
    	State expectedState = DrawerClosedPlaying.getInstance();
    	assertThat(actualState, is(sameInstance(expectedState)));
    	
    }
    @Test
    public void stopButtonPushedTest() {
    	player.changeState(DrawerClosedPlaying.getInstance());
       	player.stopButtonPushed();
    	State actualState = player.getState();
    	State expectedState = DrawerClosedNotPlaying.getInstance();
    	assertThat(actualState, is(sameInstance(expectedState)));
    	
    }
    	//System.out.println("Player State = " + player.getState());
    	//player.openCloseButtonPushed();
    	//System.out.println("Player State = " + player.getState());
    	//player.playButtonPushed();
    	//System.out.println("Player State = " + player.getState());
    	//player.openCloseButtonPushed();
    	//System.out.println("Player State = " + player.getState());
    	//player.openCloseButtonPushed();
    	//System.out.println("Player State = " + player.getState());
    	//player.playButtonPushed();
    	//System.out.println("Player State = " + player.getState());
        //player.openCloseButtonPushed();
       // System.out.println("Player State = " + player.getState());

}
