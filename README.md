# Nand2Tetris – Part 1: From Logic Gates to a CPU

This repository contains my complete implementation of **Part 1** of the [Nand2Tetris](https://www.nand2tetris.org/) project, which guides you through building a modern computer from the ground up, starting from basic logic gates all the way to a functioning CPU and assembler.

## 🔧 Contents

- ✅ HDL implementations of all required chips
- 🧠 Schematics of the **ALU** and **CPU** created using [Pranav Jain’s Nand2Tetris HDL Visualizer](https://marketplace.visualstudio.com/items?itemName=PranavJain.nand2tetris-hdl-visualizer) (VSCode extension)
- 🧾 An enhanced Assembler written in Python, featuring **error checking** even though it wasn’t required

## 🧩 Why Only ALU and CPU Schematics?

The **ALU** and **CPU** are the most complex and unique chips in this part of the project. Other components—such as basic logic gates, multiplexers, and memory chips—are either standard or trivial in nature, so I focused on illustrating the parts that benefit most from visual representation.

> ⚠️ **Important Note on Clocked Chips:**  
> Due to limitations in the Nand2Tetris HDL (and by extension the HDL Visualizer), clocked components such as `DFF`, `Register`, `PC`, `RAM`, and `ROM` could not be fully represented in the schematics. The visualizations should be interpreted with the understanding that these chips are **clock-driven**.

## 🛠 About the Assembler

Part 06 of the Nand2Tetris course requires you to build an assembler that translates Hack assembly into binary machine code, assuming the input `.asm` file is valid. While this assumption simplifies the task, I chose to implement **error checking** for the sake of practice and robustness. This means my code is more complex than strictly necessary, but it can serve as a more complete solution for those looking to go beyond the minimum.

## 📚 Learn More

You can find all official specifications, hardware definitions, machine language formats, and more at the [Nand2Tetris website](https://www.nand2tetris.org/).

---

## ✍️ Credits

- **Schematics** generated using [Pranav Jain's Nand2Tetris HDL Visualizer](https://marketplace.visualstudio.com/items?itemName=PranavJain.nand2tetris-hdl-visualizer) for VSCode — many thanks!
- Based on the *Nand2Tetris* course and book: *The Elements of Computing Systems* by Noam Nisan and Shimon Schocken

## 🖋️ Signed,

**A. Asaduz**
