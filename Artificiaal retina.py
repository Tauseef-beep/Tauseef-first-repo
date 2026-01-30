import cv2
import numpy as np
import time
from collections import deque

class ArtificialRetina:
    def __init__(self):
        # --- BIOLOGICAL CONFIGURATION ---
        self.RETINA_W, self.RETINA_H = 320, 240  # Low res M-Pathway (Rods)
        self.MIN_AREA = 800                      # Sensitivity threshold
        self.ADAPTATION_RATE = 0.02              # Synaptic plasticity (learning rate)
        self.HISTORY_LEN = 5                     # "Short term memory" for smoothing
        self.PIXEL_TO_METER_METRIC = 0.05        # Calibration for speed

        # --- MEMORY BUFFERS ---
        self.avg_frame = None
        self.position_history = deque(maxlen=self.HISTORY_LEN)
        self.area_history = deque(maxlen=self.HISTORY_LEN)
        self.prev_time = time.time()

        print("--- ARTIFICIAL RETINA ACTIVATED ---")
        print("Mimicking: M-Pathway (Motion/Depth)")
        print("Press 'q' to sever connection.")

    def mimic_ganglion_cells(self, gray_frame):
        """
        Simulates the Receptive Fields of the retina using Difference of Gaussians (DoG).
        This extracts edges and contrast just like biological ganglion cells.
        """
        # Excitatory Center (Sharp)
        g1 = cv2.GaussianBlur(gray_frame, (3, 3), 0)
        # Inhibitory Surround (Blurry)
        g2 = cv2.GaussianBlur(gray_frame, (13, 13), 0)
        # Subtract to get the "Edge/Contrast" signal
        return cv2.subtract(g1, g2)

    def calculate_dynamics(self, center, area):
        """
        Calculates Speed (X/Y) and Looming (Z-axis approach) using smoothed history.
        """
        current_time = time.time()
        dt = current_time - self.prev_time
        self.prev_time = current_time

        if dt == 0: return 0, "Static"

        # 1. Update Short Term Memory
        self.position_history.append(center)
        self.area_history.append(area)

        # We need at least 2 frames of memory to calculate change
        if len(self.position_history) < 2:
            return 0, "Analyzing..."

        # 2. Calculate Lateral Speed (Smoothed)
        # Compare current pos with the average of recent past to reduce jitter
        start_pos = self.position_history[0]
        curr_pos = self.position_history[-1]
        
        dx = curr_pos[0] - start_pos[0]
        dy = curr_pos[1] - start_pos[1]
        distance_pixels = np.sqrt(dx**2 + dy**2)
        
        # Speed = Distance / (Time elapsed for the buffer)
        # Note: This is an estimation. For strict physics, we'd sum dt history.
        speed = (distance_pixels * self.PIXEL_TO_METER_METRIC) / (dt * len(self.position_history))

        # 3. Calculate Looming (Z-Axis Motion)
        # Compare recent area average vs current area
        avg_past_area = np.mean(list(self.area_history)[:-1])
        area_delta = area - avg_past_area
        
        # Thresholds for looming state
        looming_state = "Stationary"
        if area_delta > 50:  # Growing significantly
            looming_state = "APPROACHING !!!"
        elif area_delta < -50: # Shrinking significantly
            looming_state = "Receding"

        return speed, looming_state

    def process_visual_field(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret: break

            # 1. RETINAL INPUT (Downsample & Grayscale)
            small_frame = cv2.resize(frame, (self.RETINA_W, self.RETINA_H))
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            
            # 2. GANGLION LAYER (Biological Edge Detection)
            # We process the DoG image for better edge stability than raw gray
            bio_view = self.mimic_ganglion_cells(gray)

            # 3. SYNAPTIC ADAPTATION (Background Subtraction)
            if self.avg_frame is None:
                self.avg_frame = gray.copy().astype("float")
                continue

            # Update background memory (Slow adaptation)
            cv2.accumulateWeighted(gray, self.avg_frame, self.ADAPTATION_RATE)
            
            # Detect changes (Spikes)
            frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg_frame))
            thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=4) # Dilate to merge broken blobs

            # 4. VISUAL CORTEX (Analysis)
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Setup output display
            display_frame = frame.copy()
            
            # Find the "Focus of Attention" (Largest Mover)
            focus_cnt = None
            max_area = 0
            
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > self.MIN_AREA and area > max_area:
                    max_area = area
                    focus_cnt = cnt

            if focus_cnt is not None:
                # Map low-res coords to high-res screen
                (x, y, w, h) = cv2.boundingRect(focus_cnt)
                scale_x = frame.shape[1] / self.RETINA_W
                scale_y = frame.shape[0] / self.RETINA_H
                
                X, Y, W, H = int(x*scale_x), int(y*scale_y), int(w*scale_x), int(h*scale_y)
                
                # --- CORTICAL PROCESSING ---
                center_point = (X + W//2, Y + H//2)
                object_area = W * H
                
                speed, motion_state = self.calculate_dynamics(center_point, object_area)

                # --- VISUALIZATION ---
                # Dynamic Color: RED = Danger (Fast/Approaching), GREEN = Safe
                is_danger = (speed > 50 or "APPROACHING" in motion_state)
                color = (0, 0, 255) if is_danger else (0, 255, 0)
                
                # Bounding Box
                cv2.rectangle(display_frame, (X, Y), (X + W, Y + H), color, 2)
                
                # HUD Info
                cv2.putText(display_frame, f"SPEED: {speed:.1f} u/s", (X, Y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                # Looming Indicator (The "Precisely closer/away" detector)
                cv2.putText(display_frame, f"DELTA: {motion_state}", (X, Y + H + 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

                # Draw tracking trail (Retinal Persistence)
                for i in range(1, len(self.position_history)):
                    if self.position_history[i - 1] is None or self.position_history[i] is None: continue
                    cv2.line(display_frame, self.position_history[i - 1], self.position_history[i], (0, 255, 255), 2)

            else:
                # If no movement, clear short term memory to prevent old data influencing new objects
                self.position_history.clear()
                self.area_history.clear()

            # Show the "Brain's View" vs "Retina's View"
            cv2.imshow("Artificial Retina (Output)", display_frame)
            cv2.imshow("Ganglion Cell Layer (Input)", bio_view) # Visualize the biological filter

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    retina = ArtificialRetina()
    retina.process_visual_field()
