// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import axios from 'axios';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('AAA Refactor Extension is active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json

	// Create a custom output channel for the extension
	const outputChannel = vscode.window.createOutputChannel("AAA Analysis");

	let disposable = vscode.commands.registerCommand('extension.pythonrefactortool', async () => {
		const editor = vscode.window.activeTextEditor;
		if (!editor) {return;}

		const selection = editor.selection;
		const text = editor.document.getText(selection);

		if (!text) {
			vscode.window.showInformationMessage("Please select the test code to analyze.");
			return;
		}

		vscode.window.setStatusBarMessage("$(sync~spin) Asking Gemini...", 3000);

		try {
			const repsonse = await axios.post('http://127.0.0.1:8000/analyze', {
				code: text
			});

			const report = repsonse.data.analysis_result;

			outputChannel.clear();
			outputChannel.show(true);
			outputChannel.appendLine(report);
		}
		catch (error) {
			vscode.window.showErrorMessage("Could not connect to Python Server.");
			outputChannel.appendLine("Error: " + error);
		}
	});

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
